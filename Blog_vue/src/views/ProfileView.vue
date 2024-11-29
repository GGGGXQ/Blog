<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white boder border-gray-200 text-center rounded-lg">
                <div class="flex justify-center">
                    <img :src="user.get_avatar" class="rounded-full object-cover w-36 h-36 sm:w-48 sm:h-48 mx-auto">
                </div>
                
                <p class="mt-4"><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name:'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{user.friends_count}} 朋友</RouterLink>
                    <p class="text-xs text-gray-500">{{user.posts_count}} 发布</p>
                </div>

                <div class="mt-6 justify-between">
                    <button
                        class="inline-block mr-2 py-4 px-6 bg-purple-600 text-xs text-white rounded-lg"
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id && can_send_friendship_request == true"
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
                    <RouterLink to="/profile/edit"
                        class="inline-block mr-2 py-4 px-6 bg-purple-600 text-xs text-white rounded-lg"
                        v-if="userStore.user.id === user.id"
                    >
                        修改信息
                    </RouterLink>
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
                <FeedForm 
                    v-bind:user="user" 
                    v-bind:posts="posts"
                />
            </div>

            <div
                class="p-4 bg-white boder border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" v-on:deletePost="deletePost"/>
            </div>
        </div>

        <div class="main-right col-span-1 sapce-y-4">
            <PeopleYouMayKnow />

            <Trends />

        </div>
    </div>    
</template>
<style>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { userUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import FeedForm from '../components/FeedForm.vue'

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
        FeedForm,
    },

    data() {
        return {
            posts:[],
            user: {
                id: null,
                friends_count: null,
                posts_count: null,
            },
            body:'',
            can_send_friendship_request: null,
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
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },

        
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
                        this.can_send_friendship_request = false
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
                    this.can_send_friendship_request = response.data.can_send_friendship_request
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