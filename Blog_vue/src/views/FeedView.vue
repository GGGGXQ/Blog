<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white boder border-gray-200 rounded-lg">
                <FeedForm 
                    v-bind:user="null" 
                    v-bind:posts="posts"
                    v-on:refresh-feed="getFeed"
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

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import FeedForm from '../components/FeedForm.vue';
export default {
    name: 'FeedView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm,
    },

    data() {
        return {
            posts:[],
            body:'',
        }
    },

     mounted() {
      console.log('FeedView mounted'); // 验证是否执行
      this.getFeed();
    },

    methods: {
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
        
        getFeed() {
          const cacheBuster = new Date().getTime();
          axios
            .get(`/api/posts/?_=${cacheBuster}`) // 添加时间戳参数防缓存
            .then(response => {
              this.posts = response.data
            })
            .catch(error => {
              console.log('error', error)
            })
        }
    }
}
</script>