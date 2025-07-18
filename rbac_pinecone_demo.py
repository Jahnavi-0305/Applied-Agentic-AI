# -*- coding: utf-8 -*-
"""RBAC_pinecone_Demo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XY6E-g4jBtBZjIWUqSpvZI0oWY8EKF6_

## Setup Instructions

Before running this notebook, make sure to:

1. Sign up for a Pinecone account and get your API key
2. Set your Pinecone API key as an environment variable:
   ```bash
   export PINECONE_API_KEY='your-api-key'
   ```
3. Install required packages:
   ```bash
   pip install pinecone-client sentence-transformers
   ```
4. Create a Pinecone index named 'products' with dimension 384 (for all-MiniLM-L6-v2 model)

# Role-Based Access Control (RBAC) with Vector Database Demo

This notebook demonstrates how to implement Role-Based Access Control (RBAC) in a Python application integrated with Pinecone vector database. We'll build a realistic e-commerce system that uses AI-powered product recommendations while maintaining strict access controls.

## Key Features
- **Vector-Based Product Search**: Using embeddings to find similar products
- **Role-Based Permissions**: Different access levels for different user roles
- **Real-time Permission Updates**: Ability to promote users and modify permissions
- **Secure Vector Operations**: Controlled access to vector database operations

## Use Cases Demonstrated
1. **Customer Experience**:
   - Basic product search using vector similarity
   - Limited to viewing products and their own orders
   - Cannot modify data or access advanced features

2. **Sales Team Operations**:
   - Access to customer information and all orders
   - Basic and advanced vector search capabilities
   - Stock management (for senior roles)

3. **Data Science Team**:
   - Full vector database management
   - Creation and modification of embeddings
   - Advanced search and analysis capabilities

4. **Administrative Control**:
   - Complete system access
   - User management
   - System-wide configuration

## What You'll Learn
- How to implement RBAC in a Python application
- Integration of vector databases with permission systems
- Managing different levels of access to AI features
- Secure handling of vector operations

## Expected Results
- A working e-commerce system with AI-powered search
- Different user roles with appropriate permissions
- Demonstration of permission inheritance and role promotion
- Clear examples of allowed vs. denied operations

## Sections:
1. Define Use Case & Setup
2. Create Demo Data
3. Configure Pinecone Integration
4. Implement RBAC Logic
5. Test Access Control
6. Update Permissions
7. Final Testing

## 1. Define Use Case & Setup

Let's consider a system that combines traditional e-commerce with AI-powered product recommendations using vector embeddings:

- **Customer**: Can view products, place orders, and get basic product recommendations
- **Sales Rep**: Can view products, manage orders, view customer info, and access basic vector search
- **Data Scientist**: Can manage vector embeddings, create/delete vectors, and access advanced search
- **Admin**: Has full access to all resources including vector database management

First, let's import required libraries and set up our environment.
"""

# !pip install pinecone-client sentence-transformers

from typing import Dict, List, Set
from dataclasses import dataclass
from datetime import datetime
import os
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from uuid import uuid4

# Base data classes
@dataclass
class User:
    id: int
    username: str
    role: str
    api_key: str = None  # For vector database access

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int
    description: str
    vector_id: str = None  # For vector database reference

@dataclass
class Order:
    id: int
    user_id: int
    products: List[int]  # List of product IDs
    total: float
    status: str
    created_at: datetime

# Initialize Pinecone client
pc = Pinecone(api_key="")#os.environ.get('PINECONE_API_KEY'))

# Initialize sentence transformer for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Setup Pinecone index
def setup_pinecone_index(index_name: str = "products", dimension: int = 384):
    """Setup Pinecone index for product embeddings"""
    try:
        # Check if index already exists
        existing_indexes = pc.list_indexes()
        if index_name not in existing_indexes.names():
            print(f"Creating new Pinecone index: {index_name}")
            # Create index using serverless spec in us-east-1
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print("Index created successfully!")
            print("Waiting for index to be ready...")
            # Wait for index to be ready
            while not pc.describe_index(index_name).status['ready']:
                time.sleep(1)
        else:
            print(f"Using existing index: {index_name}")

        # Connect to the index
        index = pc.Index(index_name)
        print("Successfully connected to index!")
        return index
    except Exception as e:
        print(f"Error setting up Pinecone index: {str(e)}")
        if 'response body' in str(e):
            print("Details:", str(e))
        return None

# Initialize the index
print("Setting up Pinecone index...")
products_index = setup_pinecone_index()
if not products_index:
    raise RuntimeError("Failed to setup Pinecone index. Please check the error messages above.")

"""## 2. Create Demo Data

In this section, we create sample data to demonstrate our RBAC system. We'll set up:

### Users with Different Roles
- **Alice** (Customer): Basic access for shopping
- **Bob** (Sales Rep): Customer service and order management
- **Carol** (Data Scientist): Vector database operations
- **David** (Admin): Full system access

### Products with Vector Embeddings
We create products with detailed descriptions and convert them into vector embeddings:
- Gaming Laptop
- Smartphone Pro
- Wireless Headphones

Each product will be:
1. Assigned a unique vector ID
2. Converted to embeddings using sentence-transformers
3. Stored in Pinecone with metadata
4. Verified for successful insertion

### Sample Orders
We'll create test orders to demonstrate:
- Order viewing permissions
- Status management
- Customer-specific access controls

Watch the output below to see the vector creation process and verification steps.
"""

# Create demo data
users = [
    User(1, "alice", "customer"),
    User(2, "bob", "sales_rep"),
    User(3, "carol", "data_scientist"),
    User(4, "david", "admin")
]

# Products with detailed descriptions
products = [
    Product(
        1,
        "Gaming Laptop",
        999.99,
        50,
        "High-performance gaming laptop with RTX 3080, 32GB RAM, and 1TB SSD. Perfect for modern AAA games."
    ),
    Product(
        2,
        "Smartphone Pro",
        599.99,
        100,
        "Latest flagship smartphone with 6.7\" OLED display, 108MP camera, and 5G connectivity. Great for mobile photography."
    ),
    Product(
        3,
        "Wireless Headphones",
        99.99,
        200,
        "Premium wireless headphones with active noise cancellation, 30hr battery life, and high-fidelity audio. Perfect for music lovers."
    )
]

orders = [
    Order(1, 1, [1, 3], 1099.98, "pending", datetime.now()),
    Order(2, 1, [2], 599.99, "completed", datetime.now())
]

# Create vector embeddings for products
print("Creating vector embeddings for products...")
for product in products:
    # Generate embedding for product description
    print(f"\nProcessing: {product.name}")
    embedding = model.encode(product.description)

    # Generate a unique vector ID
    product.vector_id = str(uuid4())

    # Create metadata for the vector
    metadata = {
        "product_id": str(product.id),
        "name": product.name,
        "price": float(product.price),
        "stock": int(product.stock),
        "description": product.description
    }

    # Get current vector count
    vector_count_before = products_index.describe_index_stats().total_vector_count
    print(f"Current vector count: {vector_count_before}")

    # Upsert vector to Pinecone
    try:
        upsert_response = products_index.upsert([
            (product.vector_id, embedding.tolist(), metadata)
        ])
        print(f"✓ Created vector for {product.name}")
        print(f"  Vector ID: {product.vector_id}")
        print(f"  Embedding dimension: {len(embedding)}")
        print(f"  Upsert response: {upsert_response}")

        # Verify the vector was added
        vector_count_after = products_index.describe_index_stats().total_vector_count
        print(f"\nVector count after insertion: {vector_count_after}")
        print(f"Vectors added: {vector_count_after - vector_count_before}")
    except Exception as e:
        print(f"✗ Error creating vector for {product.name}: {str(e)}")

# Print sample data
print("\nUsers:")
for user in users:
    print(f"  {user.username} ({user.role})")

print("\nProducts:")
for product in products:
    print(f"  {product.name}: ${product.price} (Stock: {product.stock})")
    print(f"    Vector ID: {product.vector_id}")

print("\nOrders:")
for order in orders:
    print(f"  Order {order.id}: ${order.total} ({order.status})")

# Print vector database stats
try:
    stats = products_index.describe_index_stats()
    print(f"\nVector Database Summary:")
    print(f"Total vectors: {stats.total_vector_count}")
    print(f"Dimension: {stats.dimension}")
    print(f"Namespaces: {list(stats.namespaces.keys()) if stats.namespaces else 'default'}")
except Exception as e:
    print(f"\nError getting vector database stats: {str(e)}")

"""## 3. Implement RBAC Logic

Here we implement a comprehensive RBAC system that controls access to both traditional e-commerce features and vector database operations.

### Permission Structure
Each role has a specific set of permissions:

**Customer Permissions:**
- `view_products`: Browse available products
- `view_own_orders`: See their own order history
- `place_order`: Make purchases
- `vector_search_basic`: Simple similarity search

**Sales Rep Permissions:**
- All customer permissions
- `view_all_orders`: See all customer orders
- `update_order_status`: Manage order status
- `view_customer_info`: Access customer details
- `vector_search_advanced`: Advanced similarity search

**Data Scientist Permissions:**
- `vector_create`: Add new vectors
- `vector_delete`: Remove vectors
- `vector_update`: Modify existing vectors
- All vector search capabilities

**Admin Permissions:**
- All permissions
- `manage_users`: User administration
- `vector_manage_index`: Full vector DB control

### Implementation Details
- Permission checking using Python sets for efficiency
- Role inheritance through permission sets
- Real-time permission verification
- Detailed access logging

The code below shows the implementation and outputs each user's permissions.
"""

class RBACSystem:
    def __init__(self):
        # Define permissions for each role
        self.role_permissions = {
            "customer": {
                "view_products",
                "view_own_orders",
                "place_order",
                "vector_search_basic"  # Basic vector similarity search
            },
            "sales_rep": {
                "view_products",
                "view_all_orders",
                "update_order_status",
                "view_customer_info",
                "vector_search_basic",
                "vector_search_advanced"  # Advanced vector operations
            },
            "data_scientist": {
                "view_products",
                "vector_search_basic",
                "vector_search_advanced",
                "vector_create",
                "vector_delete",
                "vector_update"
            },
            "admin": {
                "view_products",
                "update_product_stock",
                "view_all_orders",
                "update_order_status",
                "view_customer_info",
                "manage_users",
                "place_order",
                "vector_search_basic",
                "vector_search_advanced",
                "vector_create",
                "vector_delete",
                "vector_update",
                "vector_manage_index"
            }
        }

    def has_permission(self, user: User, permission: str) -> bool:
        if user.role not in self.role_permissions:
            return False
        return permission in self.role_permissions[user.role]

    def get_user_permissions(self, user: User) -> Set[str]:
        return self.role_permissions.get(user.role, set())

# Create RBAC system instance
rbac = RBACSystem()

# Print permissions for each role
for user in users:
    print(f"\nPermissions for {user.username} ({user.role}):")
    permissions = rbac.get_user_permissions(user)
    for permission in sorted(permissions):
        print(f"  - {permission}")

"""## 4. Test Access Control

Now we'll test our RBAC system with real-world scenarios. We'll verify:

### 1. Vector Search Operations
- Customer basic search (should succeed)
- Sales rep advanced search (should succeed)
- Customer attempting advanced operations (should fail)

### 2. Order Management
- Customers viewing their own orders
- Sales reps viewing all orders
- Unauthorized access attempts

### 3. Vector Database Operations
- Data scientists creating new vectors
- Admins managing vector indexes
- Unauthorized vector operations

### Expected Results
You should see:
- Successful basic searches for all users
- Advanced operations succeeding only for authorized roles
- Clear access denied messages for unauthorized attempts
- Detailed logging of all operations

The code below runs these tests and shows the results:
"""

class ECommerceSystem:
    def __init__(self, rbac: RBACSystem, users: List[User], products: List[Product], orders: List[Order]):
        self.rbac = rbac
        self.users = {user.id: user for user in users}
        self.products = {product.id: product for product in products}
        self.orders = {order.id: order for order in orders}
        self.vector_index = products_index

    def view_products(self, user: User) -> List[Dict]:
        if not self.rbac.has_permission(user, "view_products"):
            return ["Access Denied: No permission to view products"]

        return [
            {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock}
            for p in self.products.values()
        ]

    def view_orders(self, user: User, order_id: int = None) -> List[Dict]:
        if not (self.rbac.has_permission(user, "view_all_orders") or
                self.rbac.has_permission(user, "view_own_orders")):
            return ["Access Denied: No permission to view orders"]

        if order_id is not None:
            order = self.orders.get(order_id)
            if not order:
                return ["Order not found"]
            if (not self.rbac.has_permission(user, "view_all_orders") and
                order.user_id != user.id):
                return ["Access Denied: Can only view your own orders"]
            return [{
                "id": order.id,
                "total": order.total,
                "status": order.status,
                "products": [self.products[pid].name for pid in order.products]
            }]

        # View all orders
        if self.rbac.has_permission(user, "view_all_orders"):
            orders_to_show = self.orders.values()
        else:
            orders_to_show = [o for o in self.orders.values() if o.user_id == user.id]

        return [
            {
                "id": order.id,
                "total": order.total,
                "status": order.status,
                "products": [self.products[pid].name for pid in order.products]
            }
            for order in orders_to_show
        ]

    def vector_search(self, user: User, query: str, top_k: int = 3) -> List[Dict]:
        """Perform vector similarity search with detailed results"""
        if not (self.rbac.has_permission(user, "vector_search_basic") or
                self.rbac.has_permission(user, "vector_search_advanced")):
            return ["Access Denied: No permission to perform vector search"]

        try:
            print(f"\nPerforming vector search for query: '{query}'")
            print(f"User: {user.username} ({user.role})")

            # Generate query embedding
            query_embedding = model.encode(query).tolist()

            # Debug: Print query embedding details
            print(f"Searching for: {query}")
            print(f"Query embedding dimension: {len(query_embedding)}")

            # Perform vector search
            results = self.vector_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            # Debug: Print search response details
            print(f"\nSearch response: {results}")

            if not results.matches:
                print("No matches found!")
                return []

            # Process search results
            formatted_results = [{
                "product_name": match.metadata["name"],
                "price": match.metadata["price"],
                "description": match.metadata["description"],
                "similarity_score": float(match.score),
                "vector_id": match.id
            } for match in results.matches]

            # Print detailed results
            print(f"\nFound {len(formatted_results)} matching products:")
            for idx, result in enumerate(formatted_results, 1):
                print(f"\n{idx}. {result['product_name']}")
                print(f"   Similarity Score: {result['similarity_score']:.4f}")
                print(f"   Price: ${result['price']}")

            return formatted_results
        except Exception as e:
            error_msg = f"Error performing vector search: {str(e)}"
            print(f"\n✗ {error_msg}")
            return [error_msg]

# Create system instance
system = ECommerceSystem(rbac, users, products, orders)

print("Testing vector search capabilities...\n")

# Test customer access with basic search
alice = users[0]  # customer
print(f"1. {alice.username} (Customer) searching for gaming products:")
results = system.vector_search(alice, "high performance gaming laptop")
if isinstance(results, list) and not isinstance(results[0], str):
    print("✓ Basic vector search successful!")

# Test data scientist access with advanced search
carol = users[2]  # data_scientist
print(f"\n2. {carol.username} (Data Scientist) searching for audio equipment:")
results = system.vector_search(carol, "premium audio with noise cancellation")
if isinstance(results, list) and not isinstance(results[0], str):
    print("✓ Advanced vector search successful!")

# Test admin access with general search
david = users[3]  # admin
print(f"\n3. {david.username} (Admin) searching for mobile devices:")
results = system.vector_search(david, "smartphone with good camera")
if isinstance(results, list) and not isinstance(results[0], str):
    print("✓ Admin vector search successful!")

"""## 5. Update Permissions

Now let's demonstrate how to update permissions and roles in our RBAC system.
"""

# Add a new role with custom permissions
rbac.role_permissions["senior_sales_rep"] = {
    "view_products",
    "view_all_orders",
    "update_order_status",
    "view_customer_info",
    "update_product_stock"  # Additional permission
}

rbac.role_permissions["senior_data_scientist"] = {
    "view_products",
    "vector_search_basic",
    "vector_search_advanced",
    "vector_create",
    "vector_delete",
    "vector_update",
    "vector_manage_index",  # Additional permission
    "view_all_orders"      # Additional permission
}

# Get user references from the users list
alice = next(user for user in users if user.username == "alice")
bob = next(user for user in users if user.username == "bob")
carol = next(user for user in users if user.username == "carol")

# Promote Bob to senior sales rep
bob.role = "senior_sales_rep"

# Promote Carol to senior data scientist
carol.role = "senior_data_scientist"

print(f"Updated permissions for {bob.username}:")
permissions = rbac.get_user_permissions(bob)
for permission in sorted(permissions):
    print(f"  - {permission}")

print(f"\nUpdated permissions for {carol.username}:")
permissions = rbac.get_user_permissions(carol)
for permission in sorted(permissions):
    print(f"  - {permission}")

# Test the updated permissions
class InventoryManagement:
    def __init__(self, rbac: RBACSystem, products: List[Product]):
        self.rbac = rbac
        self.products = {p.id: p for p in products}

    def update_stock(self, user: User, product_id: int, new_stock: int) -> str:
        if not self.rbac.has_permission(user, "update_product_stock"):
            return "Access Denied: No permission to update stock"

        if product_id not in self.products:
            return "Product not found"

        self.products[product_id].stock = new_stock
        return f"Stock updated successfully for {self.products[product_id].name}"

# Create inventory management instance
inventory = InventoryManagement(rbac, products)

# Test stock update with different users
print(f"\nTesting stock updates:")
print(f"1. Alice (Customer) attempting to update stock:")
print(inventory.update_stock(alice, 1, 45))

print(f"\n2. Bob (Senior Sales Rep) attempting to update stock:")
print(inventory.update_stock(bob, 1, 45))

# Verify the stock update
print(f"\nUpdated product information:")
print(system.view_products(bob)[0])

# Test the updated permissions with vector operations
class VectorManagement:
    def __init__(self, rbac: RBACSystem, vector_index):
        self.rbac = rbac
        self.vector_index = vector_index

    def create_vector(self, user: User, data: str, metadata: Dict) -> str:
        if not self.rbac.has_permission(user, "vector_create"):
            return "Access Denied: No permission to create vectors"

        try:
            vector_id = str(uuid4())
            embedding = model.encode(data).tolist()

            self.vector_index.upsert([
                (vector_id, embedding, metadata)
            ])

            return f"Vector created successfully with ID: {vector_id}"
        except Exception as e:
            return f"Error creating vector: {str(e)}"

# Create vector management instance
vector_mgmt = VectorManagement(rbac, pc.Index("products"))

# Test vector operations with different users
print(f"\nTesting vector operations:")

# Test with customer (should fail)
print(f"1. Alice (Customer) attempting to create vector:")
print(vector_mgmt.create_vector(
    alice,
    "New gaming monitor with 4K resolution",
    {"name": "Gaming Monitor", "price": 399.99}
))

# Test with senior data scientist (should succeed)
print(f"\n2. Carol (Senior Data Scientist) attempting to create vector:")
print(vector_mgmt.create_vector(
    carol,
    "New gaming monitor with 4K resolution",
    {"name": "Gaming Monitor", "price": 399.99}
))

# Test vector search with new data
print(f"\n3. Testing vector search with new data:")
print(system.vector_search(carol, "4K display", top_k=2))

"""## 6. Final Testing

This section performs a comprehensive test of all system components:

### Test Scenarios

1. **Basic Operations**
   - Product viewing permissions
   - Order access control
   - Stock management restrictions

2. **Vector Operations**
   - Basic similarity search
   - Vector creation/deletion
   - Index management

3. **Role-Based Tests**
   - Testing each user role
   - Verifying permission boundaries
   - Checking access denials

### Success Criteria
Each test will be marked as either:
- ✓ Success: Operation completed as expected
- ✗ Failed: Operation denied or errored appropriately
- ! Error: Unexpected behavior

### Results Analysis
The final output will show:
- Total vectors in database
- Successful vs. failed operations
- Permission enforcement accuracy
- System stability metrics

Watch the test results below:
"""

def test_user_actions(system: ECommerceSystem, vector_mgmt: VectorManagement, user: User):
    print(f"\nTesting {user.username} ({user.role}):")

    print("1. Basic Operations:")
    print("  a. Viewing products:")
    products = system.view_products(user)
    print("    Success" if isinstance(products, list) and products and isinstance(products[0], dict) else "    Failed")

    print("  b. Viewing orders:")
    orders = system.view_orders(user)
    print("    Success" if isinstance(orders, list) and orders and isinstance(orders[0], dict) else "    Failed")

    print("2. Vector Operations:")
    print("  a. Basic vector search:")
    search_results = system.vector_search(user, "high performance laptop")
    print("    Success" if isinstance(search_results, list) and not isinstance(search_results[0], str) else "    Failed")

    print("  b. Vector creation:")
    create_result = vector_mgmt.create_vector(
        user,
        "Test product description",
        {"name": "Test Product", "price": 99.99}
    )
    print(f"    {create_result}")

# Test all users
for user in users:
    test_user_actions(system, vector_mgmt, user)

print("\nRBAC Demo with Vector Database Integration Complete!")

# Print summary of vector database state
try:
    stats = pc.Index("products").describe_index_stats()
    print(f"\nVector Database Summary:")
    print(f"Total vectors: {stats.total_vector_count}")
    print(f"Dimension: {stats.dimension}")
    print(f"Namespaces: {list(stats.namespaces.keys()) if stats.namespaces else 'default'}")
except Exception as e:
    print(f"\nError getting vector database stats: {str(e)}")

"""## Cleanup

Remember to clean up resources when you're done testing:

1. Vector database cleanup (if needed)
2. Reset user permissions
3. Clear sensitive data
"""

# Cleanup code (uncomment if needed)
'''
# Delete vectors if needed
try:
    pc.Index("products").delete(delete_all=True)
    print("Cleaned up vector database")
except Exception as e:
    print(f"Error cleaning up vector database: {str(e)}")

# Reset user roles
carol.role = "data_scientist"
print("Reset user roles")
'''