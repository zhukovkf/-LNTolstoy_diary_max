# Автопостинг дневника Толстого в MAX

Второй бот, параллельно с Telegram-версией. Каждые день в 09:00 МСК постит следующая запись из дневника Лева Николаевича.

## Настройка (5 минут)

### Шаг 1: Regenerate MAX_BOT_TOKEN

Если вы уже обидели токен, необходимо генерировать новый:

1. Открой https://business.max.ru
2. 2. Найди созданного бота
   3. 3. Settings → нажми кнопку regenerate для токена
      4. 4. Копируй НОВЫЙ токен
        
         5. ### Шаг 2: Адд секрет MAX_BOT_TOKEN
        
         6. 1. В этом репозиторию: **Settings**
            2. 2. **Secrets and variables** → **Actions**
               3. 3. **New repository secret**
                  4. 4. Name: `MAX_BOT_TOKEN`, Value: вставь НОВЫЙ токен
                     5. 5. **Add secret**
                       
                        6. ### Шаг 3: Узнай chat_id канала
                       
                        7. 1. Вкладка **Actions**
                           2. 2. Workflow **Get MAX chat_id (разовая настройка)**
                              3. 3. **Run workflow**
                                 4. 4. В поле `channel_link` напиши ID нашего канала (id230812641806_biz)
                                    5. 5. **Run workflow** (зелёная кнопка)
                                       6. 6. Эжди 30 сек, нажми на job → в логе есть `chat_id: <число>`. Копируй это число.
                                         
                                          7. ### Шаг 4: Add секрет MAX_CHAT_ID
                                         
                                          8. 1. Settings → Secrets and variables → Actions
                                             2. 2. **New repository secret**
                                                3. 3. Name: `MAX_CHAT_ID`, Value: <число из шага 3>
                                                   4. 4. **Add secret**
                                                     
                                                      5. ### Шаг 5: Тестирование
                                                     
                                                      6. 1. Вкладка **Actions**
                                                         2. 2. Workflow **Daily Tolstoy post (MAX)**
                                                            3. 3. **Run workflow** (зелёная кнопка)
                                                               4. 4. Эжди 30 сек → открой job → в логе есть `Опубликовано в MAX: ...`
                                                                  5. 5. Открой канал в MAX → идет первый пост.
                                                                    
                                                                     6. ## Готово!
                                                                    
                                                                     7. Дальше бот будет постить автоматически каждый день в 09:00 МСК.
