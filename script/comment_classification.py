import openai
import ast
import json
import re
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Set OpenAI API credentials
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.engine = os.getenv("OPENAI_ENGINE")


def comment_classification(comment):

    system_prompt = (
        "Review carefully and summarize the following customer's comment. "
        "Then, based on each significant point made, assign a relevant category from the following options: "
        "Branch Facilities, ABC Market Brand, Credit Limit, Customer Service, Customer Stationeries, Marketing Related, Policies Related, Pricing Related, Process & Procedure, Queue Management, SSB Related. "
        "Given the overall context of the comment, also decide the most pertinent category that encapsulates the main essence of the comment."
        "In order to enhance performance, consider indicating the location in the original text for each summarization, instead of displaying the entire text. "
        "Deposit your categorized summaries into a dictionary under the key 'Comments' as separate dictionaries, each containing 'Text_Position', 'Summary' and 'Category'. Finally, infer from the overall context and choose the category that best encompasses the main theme of the comment, and assign this under the 'Main_Category' key in your dictionary."
    ) 

    user_prompt = (
        "我係ABC Market銀行嘅長期用戶，佢們香港既分行一向都好齊備同管理有序。但係最近喺Orchard Road嘅分行我就遇見咗啲令人唔開心嘅情況。雖然我知Orchard係個人流量大嘅地方，但我真係覺得佢哋喺繁忙時段嘅佇列管理方法好有改善空間。同時，我都好欣賞ABC Market無紙化嘅政策，我最近先開始用ABC Market app希望我可以隨時隨地掌握自己嘅賬戶信息。 "
        "講到ABC Market app，我覺得佢哋嘅用戶體驗做得好好。我之前申請信用卡都係喺app度處理好，過程都算流暢。不過，我求其都希望信用額度可以彈性少少。我唔係話想亂用錢，不過有時喺出現突發嘅支出個陣，比較大嘅信用額度就可以令我更安心。我建議ABC Market可以為長期嘅忠誠客戶提供更高嘅信用卡額度。同我呢啲金融知識唔係好夠嘅用戶黎講，額度申請過程可能有少少複雜，但如果有呢個服務嘅詳情同適用條款清楚列明喺網頁上或者專人解釋，就能令我同好多其他客戶得到實質幫助。 "
        "我總體上好認同ABC Market嘅服務。我希望ABC Market可以持續改善服務同提供更多為客戶考慮嘅產品及服務。"
    )

    assistant_prompt = (
            '{ "Comments": [ '
                '{ "Summary": "The user is generally satisfied with ABC Market bank, particularly the services offered and the well-organised setup at Hong Kong branches.", "Category": "ABC Market Brand", "Text_Position": "我係ABC Market銀行嘅長期用戶，佢們香港" }, '
                '{ "Summary": "The user encounters a long queue at the Orchard Road branch during peak hours which impacts their overall experience.", "Category": "Queue Management", "Text_Position": "但係最近喺Orchard Road嘅分行我就遇見咗" }, '
                '{ "Summary": "High praise for the user-friendly ABC Market app which makes \\"paperless\\" banking convenient and efficient.", "Category": "Process & Procedure", "Text_Position": "我都好欣賞ABC Market無紙化嘅政策，我最近" }, '
                '{ "Summary": "The user expresses dissatisfaction in the assigned credit limit by ABC Market, voicing a need for larger or more flexible credit limits for customers.", "Category": "Credit Limit", "Text_Position": "我之前申請信用卡都係喺app度處理好，過程都算" }, '
                '{ "Summary": "The user feels that the procedure to apply for a higher credit limit is quite complex and suggests that ABC Market should provide clearer information or personalized guidance for users with less financial literacy.", "Category": "Policies Related", "Text_Position": "同我呢啲金融知識唔係好夠嘅用戶黎講，額度申請" } '
            '], "Main_Category": "Customer Service" }'
    )

    msg = [
        {"role":"system", "content": system_prompt},
        {"role":"user", "content": user_prompt},
        {"role":"assistant", "content": assistant_prompt},
        {"role":"user", "content": comment},
    ]
    response = openai.ChatCompletion.create(
        engine=openai.engine,
        messages=msg,
        temperature=0,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )["choices"][0]["message"]["content"]

    response = ast.literal_eval(response)

    return response

