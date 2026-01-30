const app = Vue.createApp({
    data() {
        return {
            appTitle: "Game Library",
            userName: "John Doe",
            selectedYear: "",
            selectedPlatform: "",
            games: [
                { id:1,name: "Super Mario", year: 1985, platform: "NES" },
                { id:2,name: "The Legend of Zelda", year: 1986, platform: "NES" },
                { id:3,name: "Metroid", year: 1986, platform: "NES" },
                { id:4,name: "Mega Man", year: 1987, platform: "NES" },
                { id:5,name: "Halo", year: 2001, platform: "Xbox" },
                { id:6,name: "The Witcher 3", year: 2015, platform: "PC" },
                { id:7,name: "God of War", year: 2018, platform: "PS4" }
            ],
            newGame : {name:"",year:"",platform:""}
        };
    },
    methods:{
        removeGames(gID) {
            this.games=this.games.filter(game=>game.id!==gID)
        },
        addGame() {
            if (this.newGame.name && this.newGame.year && this.newGame.platform) {
                this.games.push({
                    id: (this.games.length + 1).toString(),
                    name: this.newGame.name,
                    year: parseInt(this.newGame.year),
                    platform: this.newGame.platform
                });
                this.newGame = { name: "", year: "", platform: "" }; 
            } else {
                alert("Please fill in all fields before adding a game.");
            }
        },
        loadData(){
            fetch("https://my-json-server.typicode.com/joseccampos(gamesLibrary/games");
            rp.then(response=>{
                if(!response.ok){
                    throw new Error("Error loading games:"+response.status+" "+response.statusText);
                }
                return response.json();
                }
            ).then(data=>{
                this.games=data;
            });
            rp.catch(error=>alert("Error loading games",error));
            }}
    ,
    computed: {
        years() {
            return [...new Set(this.games.map(game => game.year))].sort();
        },
        platforms() {
            return [...new Set(this.games.map(game => game.platform))].sort();
        },
        filteredGames() {
            return this.games.filter(game => {
                return (!this.selectedYear || game.year == this.selectedYear) &&
                       (!this.selectedPlatform || game.platform == this.selectedPlatform);
            });
        },
        formFilled(){
            return this.newGame.name && this.newGame.year && this.newGame.platform
        }
}
});

app.mount("#app");
