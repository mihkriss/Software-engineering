workspace "Сайт конференции" {
    model {
        speaker = person "Докладчик"  {
            description "Пользователь, который предоставляет свои доклады на конференции"
        }
        organizer = person "Организатор"{
            description "Пользователь, который организовывает конференции"
        }
        admin = person "Администратор"{
            description "Пользователь, который следит за конференциями и управляет докладами"
        }
        guest = person "Гость"{
            description "Пользователь, который ищет доклады и является слушателем на конференции"
        }
        
        conference = softwareSystem "Сайт конференции" {
            description "Система для управления конференциями, пользователями и докладами"
            
            userActions = container "Взаимодействия пользователей с системой"  {
                description "Обрабатывает регистрацию и поиск пользователей"
                technology "FastAPI"
      
                createUser = component "Создание нового пользователя" {
                    description "Обрабатывает регистрацию и вход пользователей"
                    technology "Spring Web"
                }
                
                searchUserMask = component "Поиск пользователей по маске имя и фамилии" {
                    description "Осуществляет поиск пользователей по маске имя и фамилии"
                    technology "Spring Web"
                }
                
                searchUserLogin = component "Поиск пользователей по логину" {
                    description "Осуществляет поиск пользователей по логину"
                    technology "Spring Web"
                }
            }
                
            docladActions = container "Взаимодействия с докладами в системе" {
                description "Управляет созданием, поиском и привязкой докладов к конференциям"
                technology "FastAPI" 
                
                createDoclad = component "Создание доклада" {
                    description "Позволяет пользователям добавлять новые доклады" 
                    technology "Spring Web" 
                }
                
                listDoclad = component "Получение списка докладов" {
                    description "Выдает список всех доступных докладов" 
                    technology "Spring Web" 
                }
                
                createDocladConference = component "Добавление доклада в конференцию" {
                    description "Привязывает доклад к определенной конференции" 
                    technology "Spring Web" 
                }
            }
            
            conferenceActions = container "Взаимодействия с конференциями в системе" {
                description "Управляет созданием и поиском конференций"
                technology "FastAPI" 
                
                createConference = component "Создание конференции" {
                    description "Позволяет организаторам создавать новые конференции" 
                    technology "Spring Web" 
                }
                
                listDocladConference = component "Получение списка докладов в конференции" {
                    description "Выдает список докладов, привязанных к конференции" 
                    technology "Spring Web" 
                }
            }
            
            dbUser = container "База данных пользователей" {
                technology "PostgreSQL"
                description "База данных для хранения информации о пользователях"
            }

            dbDoclad = container "База данных докладов" {
                technology "PostgreSQL"
                description "База данных для хранения информации о докладах"
            }

            dbconference = container "База данных конференций" {
                technology "PostgreSQL"
                description "База данных для хранения информации о конференциях"
            }
        }
        
        //Взаимодействия    
        speaker -> createUser "Создание пользователя"
        createUser -> dbUser "Записывает данные о пользователях"
        
        speaker -> createDoclad "Создает и управляет докладами"
        createDoclad -> dbDoclad "Записывает данные о докладах"
        
        organizer -> createConference "Создание конференций"
        createConference -> dbconference "Записывает данные о конференциях"
        
        organizer -> createDocladConference "Создает и управляет своими докладами в конференции"
        createDocladConference -> dbDoclad "Записывает данные о докладах"
        
        admin -> conference "Управляет докладами и конференциями"
        
        guest -> createUser "Создание пользователя"
        
        guest -> searchUserMask "Поиск пользователя по имени"
        dbUser -> searchUserMask "Читает данные о пользователях по имени"
        
        guest -> searchUserLogin "Поиск пользователя по логину"
        dbUser -> searchUserLogin "Читает данные о пользователях по логину"
        
        guest -> listDoclad "Поиск доступных докладов"
        dbDoclad -> listDoclad "Читает данные о доступных докладах"
        
        guest -> listDocladConference "Поиск доступных докладов"
        dbDoclad -> listDocladConference "Читает данные о доступных докладах в конференции"
    }
    
    views {
        themes default
        
        dynamic conference "CreateDoclad" {
            speaker -> userActions "Создание/вход пользователя"
            userActions -> dbUser "Проверка учетных данных о пользователе"
            dbUser -> userActions "Ответ о пользователе"
            userActions -> speaker "Подтверждение регистрации/входа"
            speaker -> docladActions "Создание нового доклада"
            docladActions -> dbDoclad "Сохранение данных о докладе"
            organizer -> conferenceActions "Добавление доклада в конференцию"
            
            autoLayout
            
            
        }
        
        systemContext conference "ConferenceWebsite" {
            include *
            autoLayout 
        }
        
        container conference {
            include *
            autoLayout 
        }
    }
}
