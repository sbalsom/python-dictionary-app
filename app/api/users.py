from app.api import bp

@bp.route('/users', methods=['GET'])
def index():
    pass

@bp.route('/users/<int:id>', methods=['GET'])
def show():
    pass

@bp.route('/users', methods=['POST'])
def create():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update():
    pass


@bp.route('/users/<int:id>', methods=['DELETE'])
def destroy():
    pass


@bp.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@bp.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass
