import streamlit as st
import pandas as pd
import json

from azureOpenAPIAgent import query_agent, create_agent


def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


st.title("👨‍💻 Chat with your own data")
#st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
dataSource= st.radio(
        "Data Source:",
    ["localdrive", "sqldb"],
    captions = ['Upload from local computer','connect to sqldb'],horizontal=True,index=None)
uploadDestination = st.radio(
        "Upload destination:",
    ["Custom-Azure-storage", "DataProduct"],
    captions = ["Connect via SAS", "Storage account associated with DP will be selcted"],horizontal=True,index=None)

if uploadDestination == 'Custom-Azure-storage':
    st.write('You selected Custom-Azure-storage.')

if uploadDestination == 'DataProduct':
    option = st.selectbox('select the data product instance',('DP1', 'DP2', 'DP3'))

if dataSource and uploadDestination:

  st.write("Please upload your CSV file below.")

  data = st.file_uploader("Upload a CSV")

  query = st.text_area("Insert your query")

  if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(data)

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_response(decoded_response)
