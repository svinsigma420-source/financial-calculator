import { createRouter, createWebHistory } from "vue-router";
import Data_page from "./components/Data_page.vue";
import analitika from "./components/analitika.vue";
import Page_notfound from "./components/Page_notfound.vue";
import Signup from "./components/Signup.vue";
import Login from "./components/Login.vue";
import welcom from "./components/welcom.vue";

const routes = [{
    path: "/analytics",
    name: "analytics",
    component: analitika
},
{
    path: "/input",
    name: "input_data",
    component: Data_page
},
{
    path: "/:notFound(.*)",
    component: Page_notfound,
    meta:{
        title: "NotFound"
    },
    
},
{
    path : "/signup",
    name : "signup",
    component : Signup
},
{
    path: "/login",
    name: "login",
    component: Login


},{
    path: "/",
    name : "welcome",
    component : welcom
}


]

const router = createRouter({history: createWebHistory(), routes})

export default router