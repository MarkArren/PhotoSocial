var posts = new Vue({
    el: '.posts',
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
            let url = new URL(window.location.href);
            // const params = new URLSearchParams()
            // params.append("search", url.searchParams.get("search"))
            // params.append("test", "testParamter")

            axios
				.get('/searchvue/', {
                    params: {
                      "search": url.searchParams.get("search")
                    }
                })
                .then(response => (this.posts = response.data.posts))
			this.seen = false
            this.unseen = true
            console.log("Refreshing search page")
        },
        cancelAutoUpdate: function(){ clearInterval(this.timer) },
    },
    beforeDestroy() {
		this.cancelAutoUpdate();
    },
})