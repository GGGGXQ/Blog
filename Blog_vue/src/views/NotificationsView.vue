<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div
                class="p-4 bg-white boder border-gray-200 rounded-lg"
                v-for="notification in notifications"
                v-bind:key="notification.id"
                v-if="notifications.length"
            >
                {{ notification.body }}
                <button class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg" @click="readNotification(notification)">详情</button>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-else
            >
                没有未读消息
            </div>
        </div>
    </div>    
</template>

<script>
import axios from 'axios'
import { userUserStore } from '@/stores/user';

export default {
    name: 'notifications', 
    setup() {
        const userStore = userUserStore()
        return { userStore }
    },

    data() {
        return {
            notifications: [],
        }
    },

    mounted() {
        this.getNotifications()
    }, 
    
    methods: {
        getNotifications() {
            axios  
                .get('/api/notifications/')
                .then(response => {
                    this.notifications = response.data.filter(
                        notification => notification.created_for_id === this.userStore.user.id
                    )
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },
        async readNotification(notification) {
            await axios
                .post(`/api/notifications/read/${notification.id}/`)
                .then(response => {
                    if (notification.type_of_notification === 'post_like' || notification.type_of_notification === 'post_comment') {
                        this.$router.push({ name: 'postview', params: { id: notification.post_id } })
                    } else {
                        this.$router.push({name: 'friends', params: {id: notification.created_for_id}})
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}
</script>