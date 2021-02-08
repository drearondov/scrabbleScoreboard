from flask import request
from urllib.parse import urlencode

from scrabbleScoreboard.extensions import ma


class PaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    links = ma.Integer(dump_only=True)

    page = ma.Integer(dump_only=True)
    pages = ma.Integer(dump_only=True)

    per_page = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @staticmethod
    def get_url(page):

        query_args = request.args.to_dict()
        query_args["page"] = page

        return f"{request.base_url}?{urlencode(query_args)}"

    def get_pagination_links(self, paginated_objects):

        pagination_links = {
            "first": self.get_url(page=1),
            "last": self.get_url(page=paginated_objects.prev_num),
        }

        if paginated_objects.has_prev:
            pagination_links["prev"] = self.get_url(page=paginated_objects.prev_num)

        if paginated_objects.has_next:
            pagination_links["next"] = self.get_url(page=paginated_objects.next_num)

        return pagination_links
