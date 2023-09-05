
function getSurveyInfo(){
    let age = document.getElementById("age").value;
    console.log("Age: " + age);
    let gender = document.getElementById("gender").value;
    console.log("gender: " + gender);
    let field = document.getElementById("career").value;
    console.log("field: " + field);
    let ready = document.getElementById("hired?").value;
    console.log("ready: " + ready);
    let company = document.getElementById("company").value;
    console.log("company: " + company);
    let mentors = document.getElementById("mentors").value;
    console.log("mentors: " + mentors);
    let rate = document.getElementById("rate").value;
    console.log("rate: " + rate);
    let recommend = document.getElementById("net-promoter-score").value;
    console.log("recommend: " + recommend);
    // alert("Thanks so much for provinding your insights and participating in my survey!")
}

document.getElementById("submit").addEventListener("click", getSurveyInfo());
