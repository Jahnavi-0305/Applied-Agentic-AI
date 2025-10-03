"""Model Configuration Definition"""

from dataclasses import dataclass, field


@dataclass
class ModelGenerationConfig:
    """Model Configuration"""

    generation: dict = field(default_factory=dict)
    safety_filters: dict = field(default_factory=dict)
    tools: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        parameters = []
        for key, value in self.generation.items():
            parameters.append(f"{key}={value}")
        for key, value in self.safety_filters.items():
            parameters.append(f"{key}={value}")
        for key, value in self.tools.items():
            parameters.append(f"{key}={value}")
        return f"{self.__class__.__name__}: {', '.join(parameters)}"

if __name__ == "__main__":
    config = ModelGenerationConfig()
    config.generation['foo'] = 'bar'
    config.tools['foz'] = 'baz'
    print(config)
