// 公告类型声明
export interface NoticeType {
  id: number
  title: string
  description: string
  pub_date: string
  img_url: string
}
// 口味类型声明
export interface FlavorType {
  id: number
  name: string
  desc: string
}

// 菜品类型声明 酒水 炒菜
export interface DishTypes {
  id: number
  name: string
  desc: string
}
// 菜品类型
export interface DishType{
  id:number
  name:string
  price:number
  desc:string
  cover:string
  order_count:number
  type:string
}
// 用户类型
export interface UserType {
  id: number
  name: string
  password: string
  phone: string
  gender: number
  email: string
  integral: number
}
// 商家类型
export interface AdminType {
  id: number
  name: string
  password: string
  phone: string
  role: string
}
