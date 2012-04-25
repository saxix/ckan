from sqlalchemy import types, Column, Table

import meta
import domain_object

tracking_summary_table = Table('tracking_summary', meta.metadata,
        Column('url', types.UnicodeText, primary_key=True, nullable=False),
        Column('package_id', types.UnicodeText),
        Column('tracking_type', types.Unicode(10), nullable=False),
        Column('count', types.Integer, nullable=False),
        Column('running_total', types.Integer, nullable=False),
        Column('recent_views', types.Integer, nullable=False),
        Column('tracking_date', types.DateTime),
    )

class TrackingSummary(domain_object.DomainObject):

    @classmethod
    def get_for_package(cls, package_id):
        obj = meta.Session.query(cls).autoflush(False)
        obj = obj.filter_by(package_id=package_id)
        data = obj.order_by('tracking_date desc').first()
        if data:
            return {'total' : data.running_total,
                    'recent': data.recent_views}

        return {'total' : 0, 'recent' : 0}


    @classmethod
    def get_for_resource(cls, url):
        obj = meta.Session.query(cls).autoflush(False)
        data = obj.filter_by(url=url).order_by('tracking_date desc').first()
        if data:
            return {'total' : data.running_total,
                    'recent': data.recent_views}

        return {'total' : 0, 'recent' : 0}

meta.mapper(TrackingSummary, tracking_summary_table)
