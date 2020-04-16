var navbar = new Vue ({
    el: 'nav',
    data: {
        showNotifications: false
    }
})

var posts = new Vue({
    el: '#posts',
    data: {
        posts: [],
        seen: true,
        unseen: false,
    },
    // Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
    created: function(){
        this.fetchPostList();
        this.timer = setInterval(this.fetchPostList, 10000);
    },
    methods:{
        fetchPostList: function(){
            axios
				.get('/posts/')
				.then(response => (this.posts = response.data.posts))
			this.seen = false
			this.unseen = true
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
        // Sends post request to server to like post and refreshes posts
		onSubmitLike: function (submitEvent) {
			// Getting parameters
			const params = new URLSearchParams();
			params.append("id", submitEvent.target.elements.id.value);
			params.append("csrfmiddlewaretoken", submitEvent.target.elements.csrfmiddlewaretoken.value);

			// Setting self so I can call this inside of promise
			const self = this;
			axios
				.post('/', params)
				.then(function (response) {
					self.fetchPostList();
				})
				.catch(error => { });
		}
    },
    beforeDestroy() {
		this.cancelAutoUpdate();
	}
})
  