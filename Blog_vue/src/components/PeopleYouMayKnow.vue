<template>
<div class="p-4 bg-white border border-gray-200 rounded-lg mb-6" v-if="users.length > 0">
    <h3 class="mb-6 text-xl">你可能认识的TA</h3>

    <div class="space-y-4">
        <div 
            class="flex items-center justify-between"
            v-for="user in users"
            v-bind:key="user.id"
        >
            <div class="flex items-center space-x-2">
                <img :src="user.get_avatar" class="w-[40px] rounded-full object-cover w-6 h-6 sm:w-12 sm:h-12 mx-auto">

                <p class="text-xs"><strong>{{ user.name }}</strong></p>
            </div>

            <RouterLink :to=" {name: 'profile', params: {id: user.id}}" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">详情</RouterLink>
        </div>
    </div>
    
</div>

</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            users: []
        }
    }, 

    mounted() {
        this.getFriendSuggetions()
    },

    methods: {
        getFriendSuggetions() {
            axios   
                .get('api/friends/suggested/')
                .then(response => {
                    console.log(response.data)
                    this.users = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
    },
}
</script>