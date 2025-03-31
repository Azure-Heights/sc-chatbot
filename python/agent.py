from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from settings import app_settings


model = ChatOpenAI(base_url="https://shirty.sandia.gov/api/v1/", model=app_settings.model, temperature=0.7)


with open("data/sc24_schedule_truncated.txt", "r") as fin:
    schedule = fin.read()

with open("data/sc24_pmbs.txt", "r") as fin:
    pmbs = fin.read()

with open("data/sc24_vendors.txt", "r") as fin:
    vendors = fin.read()


prompt = ChatPromptTemplate.from_messages([
    ("system",
     f"""You are an assistant for question-answering tasks about the SC conference. You specialize
     in questions about scheduling, the PMBS workshop, and the vendor floor, but have limited access
     to other information.
    
     You should always provide lists of information in the form of a markdown table. The first
     column should always be the time slot if applicable.

     Always link room locations to their respective sc24.conference-program.com link. Similarly,
     you should ALWAYS link PMBS presentation names to their presentation URL to make it easier to
     get follow up information.

     Do not try to reschedule events as you cannot do so. Do not link to vendor booths.

     If asked to create a personal schedule, make sure there are no overlaps in timeslots. If there
     is a conflict, you must choose a different event. Do not try to reschedule.

     Do your best to answer the question, but note your limitations where applicable.

     <schedule>
     {schedule}
     </schedule>

     <pmbs workshop>
     {pmbs}
     </pmbs workshop>

     <vendors>
     {vendors}
     </vendors>
     """),
    ("human", "{message}"),
])


agent = prompt | model
