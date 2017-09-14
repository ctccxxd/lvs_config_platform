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
dsy.add("0",[]);