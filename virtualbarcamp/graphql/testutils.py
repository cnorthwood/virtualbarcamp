class GraphQLInfo:
    class GraphQLContext:
        def __init__(self, user):
            self.user = user

    def __init__(self, user):
        self.context = self.GraphQLContext(user)
