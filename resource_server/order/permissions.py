from rest_framework.permissions import BasePermission


class IsManagerOrCustomerForOrder(BasePermission):
    """Order 용 권한 클래스"""

    def has_permission(self, request, view):
        # `request.user`가 딕셔너리인 경우
        user_role = request.user.get("role") if isinstance(request.user, dict) else None
        print(user_role)
        if user_role == "manager":
            return True  # 관리자는 모든 액션 접근 가능

        # 고객은 GET 메소드와 POST 메소드 접근 가능
        if request.method in ["GET", "POST", "PATCH"]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # `request.user`가 딕셔너리인 경우
        if isinstance(request.user, dict):
            user_role = request.user.get("role")
            user_username = request.user.get("username")
        else:
            user_role = None
            user_username = None

        # 관리자는 모든 객체에 접근 가능
        if user_role == "manager":
            return True
        # 일반 사용자는 본인 주문에만 접근 가능
        return obj.customer.username == user_username
