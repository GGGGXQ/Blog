<template>
    <div class="mb-2 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full object-cover w-6 h-6 sm:w-12 sm:h-12 mx-auto">
            <p>
                <strong>
                    <RouterLink :to="{name:'profile', params:{ 'id': post.created_by.id }}">{{ post.created_by.name }}</RouterLink>
                </strong>
            </p>
        </div>
        <p class="text-gray-600 text-xs">{{ post.created_at_formatted }}</p>
    </div>

    <RouterLink :to="{name: 'postview', params: {id: post.id}}"><p>{{ post.body }}</p></RouterLink>
    
    <div class="my-6 flex justify-between">
        <div class="flex space-x-6">
            <div class="flex items-center space-x-2" @click="likePost(post.id)">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    :class="{'text-red-500': post.isLiked}"
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="size-6 "
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z"
                        :fill="post.isLiked? 'red':'none'"
                    />
                </svg>

                <span class="text-gray-500 text-xs">{{post.likes_count}}</span>
            </div>
            
            <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
                </svg>

                <span class="text-gray-500 text-xs">{{post.comments_count}}</span>
            </RouterLink>
        </div>
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
            </svg>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        post: Object
    },

    methods: {
        fetchPost() {
            axios
                .get(`/api/posts/`)
                .then(response => {
                    const post = response.data.find(post => post.id === this.post.id);
                    if (post) {
                        this.post.isLiked = post.is_liked
                    }
                })
                .catch(error => {
                    console.error('Error fetching post:', error);
                });
        },
        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message === 'like created') {
                        this.post.likes_count += 1
                        this.post.isLiked = true
                    } else if (response.data.message === 'dislike created') {
                        this.post.likes_count -= 1
                        this.post.isLiked = false
                    }
                })
                .catch(error => {
                    console.error('Error liking post:', error);
                })
        }
    },
    mounted() {
        this.fetchPost()
    }
}
</script>