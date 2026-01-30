console.log("Hello World");

let Obj = {
    nome:"Rui",
    idade:20,
    dizOla: function(){
        console.log("Olá "+this.nome+"!");
    },
    setNome: function(nome){
        this.nome = nome;
    },
    dizXau: function(){
        console.log("Xau "+this.nome+"!");
    },
    dizIdade: function(){
        console.log("A minha idade é "+this.idade+" anos!");
    }

}
Obj.dizOla(); 
Obj.setNome("João");
Obj.dizOla();
Obj.dizIdade();
Obj.dizXau();
