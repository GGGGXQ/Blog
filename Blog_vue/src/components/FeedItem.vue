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

    <template v-if="post.attachments.length">
        <div>
            <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mt-4 rounded-xl" @click="showImage(image.get_image)">
            <div 
                v-if="selectedImage" 
                class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
                @click="closeImage"
            >
                <img :src="selectedImage" class="max-w-full max-h-full rounded-lg">
                </div>
        </div>
    </template>

    <div class="my-6 flex justify-between"> 
        <div class="flex space-x-6 items-center">
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
            <div v-if="post.is_private=== true && userStore.user.id === post.created_by.id" class="flex items-center space-x-2 text-gray-500 text-xs">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>

                <span>仅好友可见</span>
            </div>
        </div>

        
        <div @click="toggleEtraModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
            </svg>
        </div>
    </div>
    <div v-if="this.showExtraModel">
        <div class="flex space-x-6 items-center">
            <div 
                class="flex items-center space-x-2" 
                @click="deletePost"
                v-if="userStore.user.id == post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
 
                <span class="text-red-500 text-xs">删除</span>
            </div>

            <div 
                class="flex items-center space-x-2"
                @click="reportPost"
                v-if="userStore.user.id !== post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-orange-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
                </svg>

                <span class="text-orange-500 text-xs">举报</span>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { userUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
export default {
    setup() {
        const userStore = userUserStore()
        const toastStore = useToastStore()
        return {
            userStore,
            toastStore
        }
    },

    props: {
        post: Object
    },

    emits: ['deletePost'],

    data() {
        return {
            selectedImage: null,
            showExtraModel: false,
        }
    },

    methods: {
        showImage(imageUrl) {
            this.selectedImage = imageUrl
        },

        closeImage() {
            this.selectedImage = null;
        },

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
        },
        toggleEtraModal() {
            this.showExtraModel = !this.showExtraModel
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)

            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {

                    this.toastStore.showToast(5000, '已删除', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        },  

        reportPost() {
            axios
                .post(`/api/posts/${this.post.id}/report/`)
                .then(response => {
                    this.toastStore.showToast(5000, '已举报', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log("error", error);
                })
        }
    },
    mounted() {
        this.fetchPost()
    }
}
</script>