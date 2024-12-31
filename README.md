
# Chatbot with Store Management and Recommendations

This repository contains a robust chatbot system designed for store management, customer interaction, and store recommendations. The chatbot offers seamless shopping cart management, service queries, and personalized recommendations based on user inputs. The project utilizes FastAPI, asyncio, and other modern Python libraries for an efficient and scalable solution.

## Features

- Store creation and management.
- Personalized chatbot for customer interactions.
- Shopping cart functionalities (add, view, remove, total).
- Store recommendation engine based on user needs.
- Integration with Redis for caching and optimized performance.
- Logging and saving chat histories.

## Project Structure

- `__init__.py`: Initialization file for the chatbot package.
- `base_agent.py`: Core chatbot logic for handling user queries and managing store-specific interactions.
- `create_stores.py`: Script to create diverse store configurations.
- `router.py`: API endpoints using FastAPI for handling chat requests.
- `run_agent.py`: Entry point for running the chatbot agent with recommendation functionality.
- `store_manager.py`: Handles store management, including creation, listing, and deletion.
- `store_recommender.py`: Analyzes user requirements and provides store recommendations.
- `test_chatbot.py`: Comprehensive test suite to validate chatbot functionalities.
- `tools.py`: Utilities for shopping cart management and external service interactions.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/MuazAwan/chatbot-store-management.git
   cd chatbot-store-management
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_openai_api_key
     REDIS_HOST=localhost
     REDIS_PORT=6379
     ```

5. Run the setup script to create store configurations:

   ```bash
   python create_stores.py
   ```

## Usage

1. Start the FastAPI server:

   ```bash
   uvicorn router:app --reload
   ```

2. Interact with the chatbot via API:

   - Endpoint: `/chat`
   - Method: POST
   - Parameters:
     - `store_name`: Name of the store.
     - `query`: User's query.

3. Run the agent with recommendations:

   ```bash
   python run_agent.py
   ```

4. Run tests to ensure everything is working:

   ```bash
   python test_chatbot.py
   ```

## Example

**API Request**

```json
{
    "store_name": "sports_hub",
    "query": "What are your services?"
}
```

**Response**

```json
{
    "response": "We offer Basketballs, Tennis Rackets, and Running Shoes."
}
```

## Tips for Uploading to GitHub

1. **Use `.gitignore`**:
   - Add sensitive files like `.env` to `.gitignore`.
   - Example:
     ```
     .env
     __pycache__/
     *.pyc
     *.log
     ```

2. **Write a Clear README**:
   - Include installation instructions, usage examples, and project details.

3. **Add a License**:
   - Although not provided here, you can create a license at any time.

4. **Provide Examples**:
   - Add sample requests and responses in the README.

5. **Documentation**:
   - Use docstrings and comments within the code for clarity.
   - Optionally, generate documentation using tools like Sphinx.

6. **CI/CD**:
   - Set up continuous integration with GitHub Actions to automate tests.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request with your changes.

## License

This project does not currently include a license file. You can add one to define the terms of use for your project.
