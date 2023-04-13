#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *
import streamlit as st
import time


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是您的健康小助手，有什么内科相关问题可以问我，希望可以帮到您，如果没回答上来，您可以咨询相关医师，祝您身体健康!。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':

    st.set_page_config(
        page_title="内科医疗问答系统",
        page_icon="🏥",
        initial_sidebar_state="expanded",
        # menu_items={
        #     'Get Help': 'https://www.extremelycoolapp.com/help',
        #     'Report a bug': "https://www.extremelycoolapp.com/bug",
        #     'About': "# This is a header. This is an *extremely* cool app!"
        # }
    )

    if "Graph" not in st.session_state:
        with st.spinner('请稍后，系统正在初始化...'):
            st.session_state.Graph = ChatBotGraph()
        st.success('初始化完成')
        st.balloons()
        time.sleep(2)
        st.experimental_rerun()
    st.markdown("# 基于:red[知识图谱]的内科医疗问答系统")
    st.divider()
    question = st.text_input("",placeholder="输入问题并回车")
    answer = st.session_state.Graph.chat_main(question)
    st.write(answer)
    # print('小勇:', answer)

