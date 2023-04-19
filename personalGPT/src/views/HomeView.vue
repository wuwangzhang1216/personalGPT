<template>
  <a-layout style="min-height: 100vh">
    <a-layout-sider v-model:collapsed="collapsed" collapsible>
      <h1 style="color:aliceblue; margin-left: 24px; font-size: 24px; font-family: 'Righteous', sans-serif; margin-top: 30px; margin-bottom: 30px;">
        PersonalGPT
      </h1>
      <a-menu 
      v-if="!initLoading && !keyRequired" 
      v-model:selectedKeys="selectedKeys" 
      theme="dark" 
      mode="inline"
      >
        <a-menu-item v-for="(chat, index) in conversationList"  :key="index" @click="getConversationById(chat.id)">
            <CommentOutlined style="font-size: 22px;" />
            <span>{{chat.name}}</span>
        </a-menu-item>
        <a-menu-item @click="openCreationModal">
          <a>
            + New chat
          </a>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #202020; padding: 0" />
      <a-layout-content>
        <div :style="{ padding: '24px', background: '#202020', minHeight: '360px' }">
          <div v-if="keyRequired" class="inputKeyContainer">
            <a-input-group compact>
              <h1 style="color: aliceblue; font-size: 32px; font-family: 'Righteous', sans-serif;">
                Enter your OpenAI API Key to start using the personalGPT ...
              </h1>
              <a-input v-model:value="openaiKey" style="width: calc(100% - 200px)" />
              <a-button type="primary" style="height: 48px;"  @click="checkIfKeyIsValid">Set Key</a-button>
            </a-input-group>
          </div>
          <a-row style="max-width: 1200px; margin:auto;" v-if="!keyRequired">
            <a style="font-size: 32px; margin-left: auto;" @click="openDeleteModal">
              <CloseCircleFilled />
              Delete
            </a>
            <a style="font-size: 32px; margin-left: 64px;" @click="openEditionModal">
              <ToolFilled />
              Edit
            </a>
            <a style="font-size: 32px; margin-left: 64px;" @click="downloadConversation">
              <DownloadOutlined />
              Download
            </a>
          </a-row>
          <a-list
            id="chatList"
            v-if="!keyRequired"
            class="chat-list"
            :loading="initLoading"
            item-layout="horizontal"
            :data-source="conversation"
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <template #actions>
                  <a @click="copyContent(item.content)">Copy</a>
                </template>
                <a-skeleton avatar :title="false" :loading="!!item.loading" active>
                  <a-list-item-meta
                    :description="item.content"
                  >
                    <template #title>
                      <a href="https://www.antdv.com/">{{ item.role }}</a>
                    </template>
                    <template #avatar>
                      <a-avatar v-if="item.role == 'user'" src="https://cdn-icons-png.flaticon.com/512/219/219986.png" />
                      <a-avatar v-else src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKP4lkDz9ShKLBPncE3VzTovit94Xv_XanI3WpCeh0Agt3vGBD1imjGdOrbAp_rrIwCC4&usqp=CAU" />
                    </template>
                  </a-list-item-meta>
                </a-skeleton>
              </a-list-item>
            </template>
          </a-list>
          <div class="inputContainer" v-if="!keyRequired">
            <a-input-group compact>
              <a-input v-model:value="question" style="width: calc(100% - 200px)" />
              <a-button type="primary" style="height: 48px;"  @click="askQuestion(question)">Submit</a-button>
            </a-input-group>
          </div>
        </div>
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        ©2023
      </a-layout-footer>
      <div class="backArrow">
        <UpOutlined @click="scrollToTop" />
      </div>
    </a-layout>
  </a-layout>
  <a-modal v-model:visible="creationVisible" title="Conversation Creation" @ok="handleCreation">
    <a-form :form="form" layout="vertical">
      <a-form-item label="Enter Conversation Name">
        <a-input v-model:value="conversationName" />
      </a-form-item>
    </a-form>
  </a-modal>
  <a-modal v-model:visible="editionVisible" title="Conversation Edition" @ok="handleEdition">
    <a-form :form="form" layout="vertical">
      <a-form-item label="Change Name">
        <a-input v-model:value="conversationName" />
      </a-form-item>
    </a-form>
  </a-modal>
  <a-modal v-model:visible="deleteVisible" title="Conversation Deletion" @ok="handleDeletion">
    <a-form :form="form" layout="vertical">
      <a-form-item label="Enter the conversation name to delet the conversation">
        <a-input v-model:value="conversationName"  />
      </a-form-item>
    </a-form>
  </a-modal>
  <div class="loading" v-if="initLoading || waitingForResponse">
    <img src="../assets/loading.gif" />
  </div>
</template>
<script>
import { CommentOutlined, ToolFilled, MenuFoldOutlined, MenuOutlined, DownloadOutlined, UpOutlined } from '@ant-design/icons-vue';
import CloseCircleFilled from '@ant-design/icons-vue/lib/icons/CloseCircleFilled';
import { message } from 'ant-design-vue';
import { getConversation, updateConversation, deleteConversation, getAllConversations, createConversation, changeConversationName, downloadConversation } from '../api/api.js'
export default {
  data() {
    return {
      collapsed: false,
      selectedKeys: [0],
      initLoading: false,
      loading: false,
      conversation: [],
      currentConversationId: 0,
      currentConversationName: "",
      conversationList: [],
      question: "",
      creationVisible: false,
      editionVisible: false,
      deleteVisible: false,
      conversationName: "",
      waitingForResponse: false,
      openaiKey: null,
      keyRequired: false
    }
  },
  components: {
    CommentOutlined,
    ToolFilled,
    MenuFoldOutlined,
    MenuOutlined,
    DownloadOutlined,
    CloseCircleFilled,
    UpOutlined,
},
  methods: {
    scrollToTop() {
      // scroll to top
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    },
    scrollToBottom() {
      // y scroll by 1300px
      window.scrollBy({
        top: 13000000000000,
        behavior: "smooth"
      });
    },
    openCreationModal() {
      // clear conversation name
      this.conversationName = "xxx";
      this.creationVisible = true;
    },
    openEditionModal() {
      // get current conversation name
      this.conversationName = this.currentConversationName;
      this.editionVisible = true;
    },
    openDeleteModal() {
      // get current conversation name
      this.conversationName = "";
      this.deleteVisible = true;
    },
    async handleCreation() {
      let res = await createConversation(this.conversationName);
      if (res.status === 201) {
        message.success("Conversation created!");
        this.creationVisible = false;
        await this.refreshConversationList();
      }
      else {
        message.error("Network error!")
      }
    },
    async handleEdition() {
      let res = await changeConversationName(this.currentConversationId, this.conversationName);
      if (res.status === 200) {
        message.success("Conversation name changed!");
        this.editionVisible = false;
        await this.refreshConversationList();
      }
      else {
        message.error("Network error!")
      }
    },
    async handleDeletion() {
      // check if the conversation name is correct
      if (this.conversationName !== this.currentConversationName) {
        message.error("Conversation name is incorrect!");
        return;
      }
      let res = await deleteConversation(this.currentConversationId);
      if (res.status === 200) {
        message.success("Conversation deleted!");
        this.deleteVisible = false;
        await this.refreshConversationList();
      }
      else {
        message.error("Network error!")
      }
    },
    async downloadConversation() {
      await downloadConversation(this.currentConversationId);
    },
    copyContent(content) {
      // copy content to clipboard
      navigator.clipboard.writeText(content);
      message.success("Copied to clipboard!");
    },
    async getConversationById(id) {
      let res = await getConversation(id);
      if (res.status === 200) {
        let data = await res.json();
        this.conversation = data.conversation;
        this.currentConversationId = data.id;
        this.currentConversationName = data.name;
      }
      else {
        message.error("Network error!")
      }
      await new Promise(r => setTimeout(r, 500)); 
      // scroll to bottom
      this.scrollToBottom();
    },
    async storeConversationById(id, conversation) {
      let res = await updateConversation(id, conversation);
      if (res.status === 200) {
        message.success("Conversation stored!");
      }
      else {
        message.error("Network error!")
      }
    },
    async askQuestion(question) {
      // add question to conversation
      this.conversation.push({
        role: "user",
        content: question,
      });
      // get answer from openai
      try {
        this.waitingForResponse = true;
        const answer = await this.askOpenAi(this.conversation);
        // add answer to conversation
        this.conversation.push({
          role: "assistant",
          content: answer,
        });
        this.waitingForResponse = false;
      } catch (error) {
        message.error("Network error! Or the conversation is too long!")
        // remove question from conversation
        this.conversation.pop();
        this.waitingForResponse = false;
        return;
      }
      // store conversation
      await this.storeConversationById(this.selectedKeys[0], this.conversation);
      this.waitingForResponse = false;
      // clean question
      this.question = "";
      await new Promise(r => setTimeout(r, 500)); 
      // scroll to bottom
      this.scrollToBottom();
    },
    async askOpenAi(conversation) {
        const BASE_URL = "https://api.openai.com/v1"
        const response = await fetch(`${BASE_URL}/chat/completions`, {
        method: "POST",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.openaiKey}`,
          }),
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            "messages": conversation,
            "temperature": 0.3,
            "max_tokens": 1024,
        })
      })
      const data = await response.json()
      return data.choices[0].message.content;
    },
    async checkIfKeyIsValid() {
      // check if the openai key is valid by call openai api
      const BASE_URL = "https://api.openai.com/v1"
      const response = await fetch(`${BASE_URL}/engines`, {
        method: "GET",
        headers: new Headers({
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.openaiKey}`,
          }),
      })
      const data = await response.json()
      if ("error" in data) {
        message.error("Invalid OpenAI key!");
        return;
      }
      else {
        // set openai key to cookie
        this.$cookies.set('openaiKey', this.openaiKey);
        message.success("Welcome!");
        this.keyRequired = false;
        // refresh conversation list
        await this.refreshConversationList();
        // get first conversation
        if (this.conversationList.length > 0) {
          this.selectedKeys = [this.conversationList[0].id];
          await this.getConversationById(this.selectedKeys[0]);
        }
      }
    },
    async refreshConversationList() {
      this.initLoading = true;
      this.conversationList = await getAllConversations();
      this.initLoading = false;
      await new Promise(r => setTimeout(r, 500));
      // scroll to bottom
      this.scrollToBottom();
    },
  },
  async created() {
    // check if the openai key is set
    if (this.openaiKey === null) {
      // try to get openai key from cookie
      this.openaiKey = this.$cookies.get('openaiKey');
      if (this.openaiKey === null) {
        // openai key is not set
        message.error("OpenAI key is not set!");
        this.keyRequired = true;
        return;
      }
    }
    this.initLoading = true;
    this.conversationList = await getAllConversations();
    // get first conversation
    if (this.conversationList.length > 0) {
      this.selectedKeys = [this.conversationList[0].id];
      await this.getConversationById(this.selectedKeys[0]);
    }
    this.initLoading = false;
    await new Promise(r => setTimeout(r, 500));
    // scroll to bottom
    this.scrollToBottom();
  },
}
</script>
<style>
  
</style>
