<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white boder border-gray-200 text-center rounded-lg">
                <img src="../assets/virtual_img.jpg" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">182 朋友</p>
                    <p class="text-xs text-gray-500">120 发布</p>
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
export default {
    name: 'FeedView',

    setup() {
        const userStore = userUserStore()

        return {
            userStore
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
            user: {},
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
        }
    }
}
</script>