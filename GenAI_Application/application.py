#%% Export OPENAI and LangSmith Key from .env file
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

#%% import library
import json
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from langchain_core.messages import BaseMessage
from typing import List, Optional

#%% Input & Output schema
# Input Schema: API 입력값
class UserIn(BaseModel):
    player_name: str = "이창근"
    expected_score: str = '2:0'
    attitude: str = "끈기"
    feeling: str = "기대감"

# Output Schema: API 출력값
class UserOut(BaseModel):
    id: int = Field(description="order")
    text: str = Field(description="생성된 응원 메시지")

#%% model import & init: LLM, embedding, OutputParser
## LLM
model = ChatOpenAI(model = "gpt-3.5-turbo-0125", 
                    temperature = 0.2) # temperature: 예측 변동성 최소화
embedding = OpenAIEmbeddings()
## Output Parser
output_parser = JsonOutputParser(pydantic_object=UserOut)
format_instructions = output_parser.get_format_instructions()

#%% retriever 정의 - FAISS
# Content Information: 응원가와 선수 position
player_info_filedir = 'GenAI_Application/player_info.json'
position_dict = dict([["GK", "골키퍼"], ["DF", "수비수"], ["MF", "미드필더"], ["FW", "공격수"]])
official_cheerup = [
        "영원토록 휘날려라 자줏빛투혼 모든이의 가슴속에 무궁하거라",
        "진정한 용기로써 맞서싸우면 무엇이 두려울소냐 (전진!)",
        "소름돋는 휘슬소리에 전쟁은 시작되었다", "자주색피 하나가득 너의 목에 적셔주리라", "두렵다 겁내지말고 앞으로 전진해가자",
        "모두 하나되어 승리 향해 나아가자", "아름답고 숭고한 마지막 땀방울이 떨어질 때까지 뜨거운 함성을 외쳐라!",
        "보문산 바라보는 희망의 얼굴, 백목력 새하얀 꽃 정다운 사람", "오늘도 한 마음에 조화를 이룰, 아름다운 내 고장 해 뜨는 거리",
        "우리는 대전 하나 시티즌, 승리를 위해 앞으로 나아가자",
        "오오오 시티즌 너의 뒤에 우릴 믿고 아시아로 가는 열차 하나의 힘으로 나가자"
        ]
roles_position = [
    "The goalkeeper is the only player allowed to handle the ball with their hands within the penalty area. Their primary role is to prevent the opposing team from scoring goals by stopping shots on goal.",
    "Defenders are responsible for protecting their team's goal and preventing the opposing team's forwards from scoring. They typically mark opposing forwards, intercept passes, and make tackles to regain possession of the ball. Defenders also contribute to building attacks by passing the ball to midfielders and forwards."
    "Midfielders play a central role in controlling the flow of the game and linking defense with attack. They are often involved in both defensive and offensive phases of play, supporting defenders in defense and providing passes to forwards in attack. Midfielders can be further categorized into defensive midfielders, central midfielders, and attacking midfielders based on their specific roles within the midfield."
    "Forwards, also known as strikers or attackers, are primarily responsible for scoring goals. They aim to receive passes from midfielders, dribble past defenders, and shoot on goal to score. Forwards often use their speed, agility, and skill to create scoring opportunities and put pressure on the opposing team's defense."
    ]

# Load Json file - player id, name, position
with open(player_info_filedir) as f:
    player_info = json.load(f)

def make_player_info_list(player_info):
    player_info_list = list()
    for player in player_info:
        player_info_list.append("{}의 등번호는 {}이고, 포지션은 {} 입니다.".format(player['name'], player['id'], position_dict[player['position']]))
    return player_info_list

context_info = official_cheerup + roles_position + make_player_info_list(player_info)

# Vector Store 생성
vectorstore = FAISS.from_texts(
    context_info,
    embedding = embedding,
)

# Retriever 생성
retriever = vectorstore.as_retriever()

#%% Prompt
template = """
'Daejeon Hana Citizens' is a professional soccer team in the K LEAGUE 1, based in Daejeon Metropolitan City.
You are a fan of 'Daejeon Hana Citizen'.
Please provide five messages of support in KOREAN for a specific player.

Requirements:
- Generate Five message of support.
- Each message should contain 100-150 words.
- Output format must be JSON.
- The value of the 'id' is an integer representing the order, and the value of the 'text' is the generated message.
- Use the following format for generating support messages: "PlayerName,\\nMessageContent".
- Utilize the provided content (cheer song of the 'Daejeon Hana Citizens' and the player's position).
- Consider the user's information provided for each message:
    - Expected match points (first message).
    - Current mood/emotion (second message).
    - Desired attitude for the player to show (third message).
- Ensure all messages are intended for the named player.
- Include the player's position or imply its meaning in at least two messages.
- Avoid duplicating words except for the player's name.

Example Supporting Message: (“손흥민,\\n가자 ! 1:0\\n자줏빛 투혼으로 \\n승리를 이끈다”, "ㅇㅇㅇ,\\n너를 응원해\\n언제나 너의 능력을\\n의심치 않아”, “사랑해,\\n은퇴전까지\\n항상 응원할게”)

content:
{content}

user's information:
{user_information}
  
"""

# prompt template 
prompt = ChatPromptTemplate.from_template(template=template, 
                                        format=output_parser.get_format_instructions())

#%% chain 연결
retrieval_chain = (
    {
        "content": retriever,
        "user_information":RunnablePassthrough() 
    }
    | prompt
    | model
    | output_parser
)

# %% Fast API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# app 정의
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/data/")
def generate_text(userin: dict):
    print(userin)
    user_information = "응원하려는 선수의 이름은 {}이고, 이 선수가 보여줬으면 하는 모습은 {}입니다. 예상하는 경기 결과는 {}이고, 현재 나는 {}을 느낍니다.".format(userin["player_name"], userin["attitude"], userin["expected_score"], userin["feeling"])
    while True:
        generated_data = retrieval_chain.invoke(user_information)
        print(generated_data)
        print(type(generated_data))
        if type(generated_data) == int:
            continue
        else:
            break
    return generated_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)