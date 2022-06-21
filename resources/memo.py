from http import HTTPStatus
from flask import request
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from flask_jwt_extended import jwt_required , get_jwt_identity


class MemoListResource(Resource):
    @jwt_required()
    def post(self) :
        data = request.get_json()
        user_id = get_jwt_identity()
        try :
            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into memo
                    (title,date,content,user_id)
                    values
                    (%s,%s,%s,%s);'''
                                
            record = (data['title'], data['date'], data['content'],user_id )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 503

        return {"result" : "success"}, 200

    def get(self) :
        # 쿼리 스트링으로 오는 데이터는 아래처럼 처리해준다.
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        # 디비로부터 데이터를 받아서, 클라이언트에 보내준다.
        try :
            connection = get_connection()

            query = '''select *
                    from memo
                    set is_publish = 1
                    limit '''+offset+''' , '''+limit+''';'''
            
            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요! 디비에서 가져온 timestamp 는 
            # 파이썬의 datetime 으로 자동 변경된다.
            # 문제는! 이데이터를 json 으로 바로 보낼수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            i = 0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['updated_at'] = record['updated_at'].isoformat()
                i = i + 1                

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 503


        return { "result" : "success" , 
                "count" : len(result_list) ,
                "result_list" : result_list }, 200