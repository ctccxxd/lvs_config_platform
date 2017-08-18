function Dsy(){
   this.Items = {};
};
Dsy.prototype.add = function(id,iArray){
   this.Items[id]=    iArray;
};
Dsy.prototype.Exists = function(id){
   if(typeof(this.Items[id]) == "undefined") return false;
   return true;
};
var dsy = new Dsy();
dsy.add("0",['lvs1']);
dsy.add("0_0",["10.129.35.177"]);
dsy.add("0_0_0",['8.8.8.8:8000']);
dsy.add("0_0_0_0",['All-RS', '10.0.0.7:85', '10.0.0.6:84', '10.0.0.5:83']);