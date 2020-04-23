var profile = new Vue({
    el: '.profile',
    data: {
        profile: [],
        posts: [],
        seen: true,
        unseen: false,
    },
    // Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
    created: function(){
        this.fetchProfile();
        this.timer = setInterval(this.fetchProfile, 10000);
    },
    methods:{
        fetchProfile: function(){
            username = window.location.pathname.split('/').pop()
            axios
				.get('/profile/', {
                    params: {
                      "username": username
                    }
                  })
                .then(response => (
                    this.profile = response.data.profile,
                    this.posts = response.data.posts
                    ))
			this.seen = false
            this.unseen = true
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
        onSubmitFollow: function (submitEvent) {
            // Getting parameters
			const params = new URLSearchParams();
			params.append("profile", submitEvent.target.elements.profile.value);
            params.append("csrfmiddlewaretoken", submitEvent.target.elements.csrfmiddlewaretoken.value);
            params.append("type", "follow");

			// Setting self so I can call this inside of promise
			const self = this;
			axios
				.post('/', params)
				.then(function (response) {
					self.fetchProfile();
				})
				.catch(error => { });
        },
        beforeDestroy() {
            this.cancelAutoUpdate();
        },
        isMod3: function(index){ 
            return ((index % 3) == 0)
        },
        is0: function(index){ 
            return (index == 0)
        },
        isBoth: function(index){ 
            return (this.isMod3(index) && this.is0(index))
        },
    },
    computed: {
        // a computed getter
        reversedMessage: function () {
            // `this` points to the vm instance
            return this.message.split('').reverse().join('')
        }
    }
})