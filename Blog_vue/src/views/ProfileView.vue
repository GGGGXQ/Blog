<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white boder border-gray-200 text-center rounded-lg">
                <img src="../assets/virtual_img.jpg" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name:'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{user.friends_count}} 朋友</RouterLink>
                    <p class="text-xs text-gray-500">120 发布</p>
                </div>

                <div class="mt-6 justify-between">
                    <button
                        class="inline-block py-4 px-6 bg-purple-600 text-xs text-white rounded-lg"
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id"
                    >
                        加为朋友
                    </button>
                    <button
                        class="inline-block py-4 px-6 bg-purple-600 text-xs text-white rounded-lg"
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id"
                    >
                        发送消息
                    </button>
                    <button
                        class="inline-block py-4 px-6 bg-red-600 text-xs text-white rounded-lg"
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                    >
                        退出
                    </button>
                    

                </div>

            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div
                class="bg-white boder border-gray-200 rounded-lg"
                v-if="userStore.user.id === user.id"
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="此刻在想什么"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">附加照片</a>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">发布</button>
                    </div>
                </form>
            </div>

            <div
                class="p-4 bg-white boder border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 sapce-y-4">
            <PeopleYouMayKnow />

            <Trends />

        </div>
    </div>    
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { userUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    name: 'FeedView',

    setup() {
        const userStore = userUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            posts:[],
            user: {
                id: null,
            },
            body:'',
        }
    }, 

    mounted() {
        this.getFeed()
    },

    watch: {
        "$route.params.id": {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        sendDirectMessage() {
            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log(error)
                })
        },

        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)
                    if (response.data.message == 'You have already sent a friendship request to this user.') {
                        this.toastStore.showToast(5000, '不可重复发送！', 'bg-red-300')
                    } else if (response.data.message == 'The user has already sent you a friendship request.'){
                        this.toastStore.showToast(5000, '对方已向您发送好友申请！', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, '请求已发送！', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error:', error)
                })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data.posts)
                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        logout() {
            console.log('Log out')
            this.userStore.removeToken()
            this.$router.push('/login')
        }
    }
}
</script>