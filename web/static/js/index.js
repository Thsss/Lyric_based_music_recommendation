var app = new Vue({ 
    el: '#app',
    data: {
        message: 'Hello Vue!',
        content: '',
        home: true,
        rec: false,
        table: false,
        items: [],
    },
    methods: {
    	navClick(but){
    		switch(but){
    			case 'home':
    				this.home = true;
    				this.rec = false;
    				break;
    			case 'rec':
    				this.home = false;
    				this.rec = true;
    				break;
    		}
    	},
    	search(cont){
    		g = this;
			axios.get('/search', {
				params: {
				  content: cont
				}
			}).then(function (response) {
				console.log(response.data);
				g.items = response.data;
				g.table = true;
			}).catch(function (error) {
				console.log(error);
			});
    	},

    	external(web){
    	    window.open('//'+web);
    	}
    }

});
