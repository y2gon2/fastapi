import socket
import threading
import json
import time

# 서버 설정
HOST = '127.0.0.1'  # 서버 IP 주소
PORT = 8889             # 서버 포트 번호

TIME_INTERVAL = 1

# JSON 데이터 생성
data = {"robot_id": 5, "state": ""}
s1 = "cargo close empty"
s2 = "cargo open empty"
s3 = "cargo open full"
s4 = "cargo close full"

def send_data(client_socket, data):
    counter = 1
    """서버에 데이터를 지속적으로 전송하는 함수"""
    try:
        while True:

            if counter % 4 == 1:
                data["state"] = s1
            elif counter % 4 == 2:
                data["state"] = s2
            elif counter % 4 == 3:
                data["state"] = s3
            else:
                data["state"] = s4

            print(data)
            # JSON 데이터를 문자열로 변환 및 인코딩 후 전송
            json_data = json.dumps(data)
            json_data += '\n'
            client_socket.sendall(json_data.encode('utf-8'))
            # print("Data sent to server:", json_data)
            
            # 1초 대기
            time.sleep(TIME_INTERVAL)
            counter += 1
    except Exception as e:
        print(f"Send thread error: {e}")

def receive_data(client_socket):
    """서버로부터 데이터를 수신하고 출력하는 함수"""
    try:
        while True:
            # 서버로부터 데이터 수신 (최대 4096 바이트)
            response = client_socket.recv(4096)
            if not response:
                # 서버가 연결을 종료한 경우
                print("Server closed the connection.")
                break
            try:
                # 수신한 데이터를 디코딩하고 JSON으로 변환
                json_response = json.loads(response.decode('utf-8'))
                print("Received from server:", json_response)
                time.sleep(TIME_INTERVAL)
            except json.JSONDecodeError:
                print("Received non-JSON data:", response.decode('utf-8'))
    except Exception as e:
        print(f"Receive thread error: {e}")

def main():
    # TCP 클라이언트 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    # 송신 스레드 시작
    send_thread = threading.Thread(target=send_data, args=(client_socket, data), daemon=True)
    send_thread.start()

    # 수신 스레드 시작
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,), daemon=True)
    receive_thread.start()

    try:
        while True:
            # 메인 스레드는 무한 루프로 대기
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
        main()
