import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'ant-design-vue/dist/antd.variable.min.css';
import { ConfigProvider } from 'ant-design-vue';
import './assets/style.css'
import VueCookies from 'vue3-cookies';

ConfigProvider.config({
  theme: {
    primaryColor: '#989898',
  },
});

import { Upload, Input, Button, Row, PageHeader, InputNumber, Skeleton,
    Statistic, Form, Descriptions, List, Table, Carousel, Avatar, Empty,
    TabPane, Tabs, Menu, Tag, Layout, Image, Select, Spin, Pagination,
  Checkbox, Progress, Comment, Slider, Dropdown, LayoutSider, Modal } from 'ant-design-vue';



const app = createApp(App)

app.use(router)
app.use(Upload)
app.use(Input)
app.use(Button)
app.use(Row)
app.use(PageHeader)
app.use(InputNumber)
app.use(Skeleton)
app.use(Statistic)
app.use(Form)
app.use(Descriptions)
app.use(List)
app.use(Table)
app.use(Carousel)
app.use(Avatar)
app.use(Empty)
app.use(TabPane)
app.use(Tabs)
app.use(Menu)
app.use(Tag)
app.use(Layout)
app.use(Image)
app.use(Select)
app.use(Spin)
app.use(Pagination)
app.use(Checkbox)
app.use(Progress)
app.use(Comment)
app.use(Slider)
app.use(Dropdown)
app.use(LayoutSider)
app.use(Modal)
app.use(VueCookies)

app.mount('#app')
