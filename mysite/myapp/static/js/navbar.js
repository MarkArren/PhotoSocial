var navbar = new Vue ({
    el: 'nav',
    data: {
        showNotifications: false,
        hasNotifications: false,
        notifications: []
    },
    // Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
    created: function(){
        this.fetchNotificationList();
        this.timer = setInterval(this.fetchNotificationList, 10000);
    },
    methods:{
        fetchNotificationList: function(){
            axios
				.get('/notifications/')
                .then(response => (this.notifications = response.data.notifications))
            if (this.notifications.length == 0){
                this.hasNotifications = false
            }else{
                this.hasNotifications = true
            }
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
        toggleNotifications: function(){
            this.showNotifications = !this.showNotifications
            this.fetchNotificationList()

            // Start auto refreshing quicker when open
            if (this.showNotifications == true){
                this.cancelAutoUpdate
                this.timer = setInterval(this.fetchNotificationList, 3000);
            }else{
                this.cancelAutoUpdate
                this.timer = setInterval(this.fetchNotificationList, 10000);
            }

        },
    },
    beforeDestroy() {
		this.cancelAutoUpdate();
	},
})

