<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg">

                <div class="space-y-4">
                    <div
                        class="flex items-center justify-between"
                        v-for="conversation in conversations"
                        v-bind:key="conversation.id"
                        v-on:click="setActiveConversation(conversation.id)"
                    >
                        <div class="flex items-center space-x-2">
                            <template
                                v-for="user in conversation.users"
                                v-bind:key="user.id"
                            >
                                <div v-if="user.id !== userStore.user.id" class="flex items-center space-x-2">
                                    <img src="../assets/virtual_img.jpg" class="w-[40px] rounded-full" />
                                    <p class="text-xs font-bold">{{ user.name }}</p>
                                </div>
                            </template>
                        </div>

                        <span class="text-xs test-gray-500">{{conversation.modified_at_formatted}}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white boder boder-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <template 
                        v-for="message in activeConversation.messages"
                        v-bind:key="message.id"
                    >
                        <div
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.created_by.id === userStore.user.id"
                        >
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">{{message.body}}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{message.created_at_formatted}}</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="../assets/virtual_img.jpg" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div 
                            class="flex w-full mt-2 space-x-3 max-w-md"
                            v-else
                        >
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="../assets/virtual_img.jpg" class="w-[40px] rounded-full">
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="test-sm">{{message.body}}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{message.created_at_formatted}}</span>
                            </div>
                        </div>
                    </template>

                    
                </div>
            </div>

            <div class="bg-white boder border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="请输入文字"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-end">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">发送</button>
                    </div>
                </form>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { userUserStore } from '@/stores/user'
export default {
    name: 'chat', 

    setup() {
        const userStore = userUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            conversations: [],
            activeConversation: {},
            body: '',
        }
    },

    mounted() {
        this.getConversations()
    },

    methods: {
        getConversations() {
            console.log('getConversations')

            axios
                .get('/api/chat/')
                .then(response => {
                    console.log(response.data)

                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation = this.conversations[0].id
                    }

                    this.getMessages()
                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            console.log('getMessages')

            axios
                .get(`/api/chat/${this.activeConversation}/`)
                .then(response => {
                    console.log(response.data)

                    this.activeConversation = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)
            axios
            .post(`/api/chat/${this.activeConversation.id}/send/`, {
                    body: this.body
                })
                .then(response => {
                    console.log(response.data)

                    this.activeConversation.messages.push(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log(error)
                })
        },

        setActiveConversation(id) {
            console.log('setActiveConversation', id)

            this.activeConversation = id
            this.getMessages()
        },
    }
}

</script>