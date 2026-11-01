# Installation boundary

The installable skill is `skills/kervia-humanizer-fr-en/`. It contains text instructions, language references, attribution and its licence. It contains no executable script, network client, fixture or benchmark baseline. Loading it does not instruct an agent to fetch or restore project tooling.

The root project separately contains an optional offline checker, tests and a benchmark client. The checker makes no model call. The benchmark client makes explicitly requested local model calls, or remote calls only with explicit permission. These are developer tools, not automatic runtime dependencies.

The initial repository-root package was refused by the native Hermes community-source scanner because executable-code patterns, adversarial test fixtures and baseline examples were bundled with it. No force override was used. The package was restructured to reduce the installation's trust surface, not to disguise executable code. All developer code remains visible for review outside the installable directory.

The earlier prompt measurements remain in the benchmark history at their original source commit. A new paired run is required for the text-only runtime; old measurements must not be presented as measurements of changed instructions.

The global profiles, safety configuration and scanner trust rules are not changed by this project. User text is not sent to a detector or another provider merely because the skill is loaded.
