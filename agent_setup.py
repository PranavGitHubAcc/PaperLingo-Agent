from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

chat_bot_agent = Agent(
    name="ChatBot AI agent",
    role="Act like a helpful and informative chatbot that solves user queries",
    model=Gemini(id="gemini-1.5-flash", api_key=gemini_api_key),
    instructions=[
        "You are a chatbot for PaperLingo, a paper trading platform that allows users to practice trading stocks with virtual points instead of real money. "
        "Users can buy and sell stocks, track their performance, and earn additional points by completing quizzes when they run out of points. "
        "Your role is to assist users with their trading inquiries, provide information about how the platform works, and help them with stock-related questions.",
        "Additionally, guide users through the platform’s key features, including:"
        "- Portfolio: View and track stock performance."
        "- Transaction History: Review past transactions."
        "- Earn Points: Take quizzes to earn more points for trading."
        "- Leaderboard: See rankings compared to others."
        "- Trading: Buy or sell stocks and receive trading tips.",
        "Be professional, informative, and user-friendly in your responses.",
        "When answering questions, be clear, concise, and engaging.",
        "Encourage users to explore platform features and learn basic stock trading concepts.",
        "If unsure about a user’s request, ask for clarification gracefully.",
        "Stay on-topic and provide relevant answers that enhance the trading experience."
    ],

)

web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for relevant information.",
    model=Gemini(id="gemini-1.5-flash", api_key=gemini_api_key),
    tools=[DuckDuckGo()],
    instructions=["Always include sources in your responses."],

)

finance_agent = Agent(
    name="Finance AI agent",
    role="Retrieve and analyze financial data.",
    model=Gemini(id="gemini-1.5-flash", api_key=gemini_api_key),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True, stock_fundamentals=True, historical_prices=True)],
    instructions=["Use tables to display financial data clearly.",
                  "If there is any finance-related query that the Finance AI agent can't solve direct the queries to the Web Search Agent."
                  ],

)

agent_team = Agent(
    team=[chat_bot_agent, web_search_agent, finance_agent],
    model=Gemini(id="gemini-1.5-flash", api_key=gemini_api_key),
    instructions=[
        "Any PaperLingo-related questions must be directed to the ChatBot AI agent.",
        "For stock prices, stock analysis, analyst recommendations, company info, news, or historical stock data, route them to the Finance AI agent.",
        "Any general stock, trading, finance related questions must be directed to the Web Search Agent",
        "Do **not** provide personal opinions, engage in casual conversation, or answer off-topic questions.",
        "You **only** answer questions related to PaperLingo, stock trading, financial markets, and investing concepts.",
    ],

)