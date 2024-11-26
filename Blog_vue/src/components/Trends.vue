<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">热门话题</h3>

        <div class="space-y-4">
            <div 
                class="flex items-center justify-between"
                v-for="trend in trends"
                v-bind:key="trend.id"
            >
                <div class="flex items-center space-x-2">
                    <p class="text-xs">
                        <strong>#{{trend.hashtag}}</strong><br>
                        <span class="text-gray-500">{{trend.occurences}} 发布</span>
                    </p>
                </div>

                <RouterLink :to="{name: 'trendview', params: {id: trend.hashtag}}" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">详情</RouterLink>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'trends',
    data() {
        return {
            trends: []
        }
    },


    mounted() {
        this.getTrends()
    },

    methods: {
        getTrends() {
            axios   
                .get('/api/posts/trends/')
                .then(response => {
                    this.trends = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>