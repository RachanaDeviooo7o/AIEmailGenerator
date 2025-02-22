import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.llms import CTransformers
from langchain_core.output_parsers import JsonOutputParser

def getLLMResponse(from_input,email_sender,email_recipient,email_style):
    # llm=CTransformers(model="llama-2-7b-chat.ggmlv3.q8_0.bin",
    #                   model_type="llama",
    #                   config={'max_new_tokens':256,'temperature':0.01 })
    llm=ChatGroq(temperature=0,groq_api_key="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",model_name="llama-3.3-70b-versatile")
    
    template="""Write an email with {style} style and included topic:{email_topic}.\n\nSender :{sender}\nRecipient :{recipient}
                            \n\nEmail Text"""
    #Creating a final prompt
    prompt=PromptTemplate.from_template(template)
    # (input_variables=["Style","email_topic","sender","recipient","email_body"],template=template)

    # response=llm(prompt.format(email_topic=from_input,sender=email_sender,recipient=email_recipient,style=email_style))
    # print(response)
    chain_extract= prompt|llm
    response=chain_extract.invoke(input={"email_topic":from_input,"sender":email_sender,"recipient":email_recipient,"style":email_style})
  
    # jsonparser=JsonOutputParser()
    # response=jsonparser.parse(response.content)
    # return response if isinstance(response.list) else response
    return response.content

st.set_page_config(page_title="Generate Emails", page_icon="✉️",
                        layout="centered")
st.header("Generate Emails")


from_input=st.text_area("Enter the email body here",height=275)
col1,col2,col3=st.columns([10,10,5])
with col1:
    email_sender=st.text_input("Enter the sender's name")
    with col2:
        email_recipient=st.text_input("Enter the recipient's name")
        with col3:
            email_style=st.selectbox("Writing style",["formal","informal","Appreciation","Apology","Complaint","Request","Suggestion"])

        submit=st.button("Generate Email")
        if submit:
            st.write(getLLMResponse(from_input,email_sender,email_recipient,email_style))
