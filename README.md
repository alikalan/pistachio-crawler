# PistachioCrawler API

Welcome to the PistachioCrawler API repository! This API scrapes data from the online shop DM to check the availability of the product "KoRo Pistazienschnitte mit 45 % Pistazie" in their branches.

## Overview

This project consists of two main components:
1. **API** (this repository) - Scrapes data from the DM online shop to check product availability.
2. **Telegram Bot** ([pc_telbot repository](https://github.com/alikalan/pc_telbot)) - Handles user interactions on Telegram to provide product availability updates.

## Features

- Scrape product availability data from the DM online shop.
- Provide API endpoints for checking the availability of the specified product.

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Clone the Repository

```bash
git clone https://github.com/alikalan/pistachio-crawler.git
cd pistachio-crawler
```

### Install Dependencies

```bash
make install
```

## Usage

### Running the API

To run the API, execute:

```bash
make run_api
```

### Docker Deployment

### Build the Docker Image

```bash
make docker_build
```

### Run the Docker Container

```bash
make docker_run
```

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Related Projects

- [PistachioCrawler Telegram Bot](https://github.com/alikalan/pc_telbot) - The Telegram bot that interacts with users to provide product availability updates.
