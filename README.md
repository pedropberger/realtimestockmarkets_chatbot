# realtimestockmarkets_chatbot
AI agent available in a conversational interface that can help the user get real-time information about stock markets and perform mathematical operations.


Objective
Create an AI agent available in a conversational interface that can help the user get
real-time information about stock markets and perform mathematical operations.
Example
These are the kind of questions the Agent should be able to respond to. They are just
inspirational, we are not going to evaluate the accuracy of answers.
➔
➔
User: "What was the Bitcoin price yesterday?"
Agent: "The closing price of Bitcoin yesterday was $59,756.70. Do you need more
details on Bitcoin's price trends?"
➔
➔
User: "And the current price of Tesla?"
Agent: "The current price of Tesla stock is $720.34. Would you like to know more about
Tesla's performance or compare it with another stock?"
➔
➔
User: "What's the percentage change compared to yesterday?"
Agent: "The price of Tesla stock increased by 2.5% compared to yesterday.
”
➔
➔
User: "Can you calculate the average stock price of Apple over the last week?"
Agent: "The average stock price of Apple over the last week was $145.67. Would you
like to see a detailed breakdown?"
Guidelines
● Integrate the OpenAI API to power the AI agent. If you don't have one, you can create a free Groq
account and get an API Key to use open source models.
● Use Streamlit to build a simple chat interface. Build a basic LLM chat app - Streamlit Docs. Feel free
to copy paste the code.
● For implementing the agentic workflow, you can interact directly with the Open AI API or use a
framework like LangChain or similar.
● Utilize the yfinance Python package to fetch real-time market data, such as stock prices &
historical data.
● Provide a Dockerfile in your project to build the environment for your Streamlit app.