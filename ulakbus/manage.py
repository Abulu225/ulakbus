#!/usr/bin/env python
# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.


from zengine.management_commands import *
from ulakbus.lib.unitime import *
from ulakbus.lib.fake import *


class CreateUser(Command):
    CMD_NAME = 'create_user'
    HELP = 'Creates a new user'
    PARAMS = [
        {'name': 'username', 'required': True, 'help': 'Login username'},
        {'name': 'password', 'required': True, 'help': 'Login password'},
        {'name': 'abstract_role', 'default': 'BaseAbsRole', 'help': 'Name of the AbstractRole'},
        {'name': 'super', 'action': 'store_true', 'help': 'This is a super user'},
        {'name': 'permission_query', 'default': "code:crud* OR code:login* OR code:logout*",
         'help': 'Permissions which will be returned from this query will be granted to the user. '
                 'Defaults to: "code:crud* OR code:login* OR code:logout*"'},
    ]

    def run(self):
        from ulakbus.models import AbstractRole, User, Role, Permission
        if User.objects.filter(username=self.manager.args.username).count():
            print("User already exists!")
            return
        abs_role, new = AbstractRole.objects.get_or_create(name=self.manager.args.abstract_role)
        user = User(username=self.manager.args.username, superuser=self.manager.args.super)
        user.set_password(self.manager.args.password)
        user.save()
        role = Role(user=user, abstract_role=abs_role)
        role.save()
        perm_list = []
        for perm in Permission.objects.raw(self.manager.args.permission_query):
            role.Permissions(permission=perm)
            perm_list.append(perm.name)
        role.save()
        user_type = 'super user' if self.manager.args.super else 'user'
        print("New %s created with these permissions: \n\n%s" % (user_type, "\n".join(perm_list)))


class LoadFixture(Command):
    CMD_NAME = 'load_fixture'
    HELP = 'Load fixtures from given json file or files in given directory and ' \
           'dumps into ulakbus_settings_fixtures bucket, overwriting data of all existing keys.'
    PARAMS = [
        {'name': 'path', 'required': True, 'help': 'Load fixture file or directory'},
    ]

    def run(self):
        from pyoko.db.connection import client
        import os

        fixture_bucket = client.bucket_type('catalog').bucket('ulakbus_settings_fixtures')
        path = self.manager.args.path

        if os.path.isdir(path):
            from glob import glob
            for fixture_file in glob(os.path.join(path, "*.json")):
                self.dump(fixture_file, fixture_bucket)
        else:
            self.dump(path, fixture_bucket)

    @staticmethod
    def dump(fixture_file, fixture_bucket):
        try:
            with open(fixture_file) as f:
                import json
                try:
                    fixtures = json.load(f)
                    for fix in fixtures:
                        f = fixture_bucket.get(fix)
                        f.data = fixtures[fix]
                        print("%s: %s stored.." % (fix, fixtures[fix]))
                        f.store()
                except ValueError as e:
                    print("please validate your json file: %s" % e)
        except IOError:
            print("file not found: %s" % fixture_file)


class GenerateBuildingList(Command):
    CMD_NAME = 'generate_buildings'
    HELP = 'Generates fake Building model objects from Unit Faculties'
    PARAMS = []

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        fake = FakeDataGenerator()
        bina_list, room_list = fake.yeni_bina()
        print("%s adet bina oluşturuldu, oluşturulan binalar: %s\n" % (len(bina_list), bina_list))
        print("%s adet oda oluşturuldu, oluşturulan odalar: %s\n" % (len(room_list), room_list))


class GenerateRandomPersonel(Command):
    CMD_NAME = 'random_personel'
    HELP = 'Generates Random Personel'
    PARAMS = [

        {'name': 'length', 'required': False, 'help': 'Amount of random personel', 'default': 1},

    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        length = int(self.manager.args.length)
        fake = FakeDataGenerator()
        fake.yeni_personel(personel_say=length)


class GenerateRandomOkutman(Command):
    CMD_NAME = 'random_okutman'
    HELP = 'Generates Random Okutman From Personel Objects'
    PARAMS = [
        {'name': 'personel', 'required': True, 'help': 'Personel object'},
    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        personel = self.manager.args.personel
        fake = FakeDataGenerator()
        fake.yeni_okutman(personel=personel)


class GenerateRandomHariciOkutman(Command):
    CMD_NAME = 'random_harici_okutman'
    HELP = 'Generates Random Okutman From Personel Objects'
    PARAMS = [

        {'name': 'length', 'required': True, 'help': 'Amount of random harici okutman', 'default': 1},

    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        length = int(self.manager.args.length)
        fake = FakeDataGenerator()
        fake.yeni_harici_okutman(harici_okutman_say=length)


class GenerateRandomOgrenci(Command):
    CMD_NAME = 'random_ogrenci'
    HELP = 'Generates Random Ogrenci Model Objects'
    PARAMS = [
        {'name': 'length', 'required': False, 'help': 'Amount of random ogrenci', 'default': 1},
    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        length = int(self.manager.args.length)
        fake = FakeDataGenerator()
        ogrenci_list = fake.yeni_ogrenci(ogrenci_say=length)
        print("Toplam %s adet ogrenci oluşturuldu, oluşturulan öğrenci listesi : %s" % (length, ogrenci_list))


class GenerateProgramList(Command):
    CMD_NAME = 'generate_programs'
    HELP = 'Generates Program Records From Unit Object'
    PARAMS = [
        {'name': 'length', 'required': False, 'help': 'Amount of random program', 'default': 1},
        {'name': 'yoksis_program', 'required': True, 'help': 'Unit object'},
    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        length = int(self.manager.args.length)
        yoksis_program = self.manager.args.yoksis_program
        fake = FakeDataGenerator()
        fake.yeni_program(yoksis_program=yoksis_program, program_say=length)


class GenerateDersList(Command):
    CMD_NAME = 'generate_ders'
    HELP = 'Generates fake Ders model objects'
    PARAMS = [
        {'name': 'length', 'required': False, 'help': 'Amount of random program', 'default': 1},
        {'name': 'program', 'required': True, 'help': 'Program object'},
        {'name': 'personel', 'required': True, 'help': 'Personel object'},
    ]

    def run(self):
        from tests.fake.fake_data_generator import FakeDataGenerator
        length = int(self.manager.args.length)
        personel = self.manager.args.personel
        program = self.manager.args.program
        fake = FakeDataGenerator()
        fake.yeni_ders(program=program, personel=personel, ders_say=length)


class GenerateZatoServiceJson(Command):
    CMD_NAME = 'generate_services_json'
    HELP = "Creates new channels and uploads services to Zato."
    PARAMS = [
        {'name': 'path', 'required': True,
         'help': 'The zato service file or folder to be installed.'},
    ]
    py_files_path = []

    def get_py_files_path(self, path):
        """
        servicelerin bulundugu klasorlerde arama yaparak .py dosyalarini bulur.
        Args:
            path: management komutunun --path parametresinden gelir

        Returns: path parametresine e gore servis veya servislerin path uzantilarini
        py_files_path dizisine ekler.

        """
        from glob import glob

        for g in glob(path+'/*'):
            file_name_extension = os.path.splitext(os.path.basename(g))[1]
            if file_name_extension == '.py':
                self.py_files_path.append(g)
            elif not file_name_extension:
                self.get_py_files_path(g)

    def run(self):
        import importlib
        import inspect
        import json
        from zato.server.service import Service

        services = []
        path = self.manager.args.path
        self.get_py_files_path(path)
        paths = self.py_files_path
        for p in paths:
            name = os.path.splitext(os.path.basename(p))[0]
            # Ignore __ files
            if name.startswith("__"):
                continue
            pth = os.path.splitext(p)[0]
            module_name = '.'.join(pth.split('/'))
            module = importlib.import_module(module_name)
            for obj_name in dir(module):
                obj = getattr(module, obj_name)
                # Eger obj bir class ise, zato `Service`  inherited ise,
                #  ve Service in kendisi degilse
                if inspect.isclass(obj) and issubclass(obj, Service) and obj is not Service \
                        and hasattr(obj, "DEPLOY") and obj.DEPLOY:
                    services.append([obj_name, obj, p])
                    continue

        zato_json = dict()
        zato_json['cluster_id'] = 1
        zato_json['SERVICES'] = []
        for name, service, path in services:
            payload_service = self.get_service_payload_data(path)
            payload_channel = self.get_channel_payload_data(service)

            zato_json['SERVICES'].append({
                "DEPLOY": service.DEPLOY,
                "CHANNEL": payload_channel,
                "SERVICE": payload_service})

        with open(os.getcwd()+'/services/json/zato.json', 'w') as outfile:
            json.dump(zato_json, outfile, indent=4)

    def get_service_payload_data(self, path):
        import base64

        with open(path, 'r') as f:
            text = f.read()
            payload = base64.b64encode(text)

        service_payload = dict()
        service_payload["name"] = os.path.splitext(os.path.basename(path))[0]
        service_payload["payload_name"] = os.path.basename(path)
        service_payload["payload"] = payload

        return service_payload

    def get_channel_payload_data(self, service):

        payload_channel = dict()
        payload_channel['name'] = service.CHANNEL_NAME
        payload_channel['connection'] = service.CONNECTION
        payload_channel['data_format'] = service.DATA_FORMAT
        payload_channel['url_path'] = service.URL_PATH
        payload_channel['transport'] = service.TRANSPORT
        payload_channel['is_active'] = service.IS_ACTIVE
        payload_channel['is_internal'] = service.IS_INTERNAL

        return payload_channel


class CreateUlakbusServiceModel(Command):
    CMD_NAME = 'create_ulakbus_services_model'
    HELP = "Creates new channels and uploads services to Zato."

    def run(self):
        import json
        from ulakbus.services.models.ulakbus_services import UlakbusService

        with open(os.getcwd()+'/services/json/zato.json', 'r') as f:
            json_data = f.read()
            data = json.loads(json_data)
            cluster_id = data['cluster_id']
            for d in data['SERVICES']:
                ulakbus_service = UlakbusService()
                ulakbus_service.cluster_id = cluster_id
                ulakbus_service.service_name = d["SERVICE"]["name"]
                ulakbus_service.service_payload_name = d["SERVICE"]["payload_name"]
                ulakbus_service.service_payload = d["SERVICE"]["payload"]
                ulakbus_service.channel_name = d["CHANNEL"]["name"]
                ulakbus_service.channel_connection = d["CHANNEL"]["connection"]
                ulakbus_service.channel_url_path = d["CHANNEL"]["url_path"]
                ulakbus_service.channel_connection = d["CHANNEL"]["connection"]
                ulakbus_service.channel_data_format = d["CHANNEL"]["data_format"]
                ulakbus_service.channel_is_active = d["CHANNEL"]["is_active"]
                ulakbus_service.channel_transport = d["CHANNEL"]["transport"]
                ulakbus_service.channel_is_internal = d["CHANNEL"]["is_internal"]
                ulakbus_service.deploy = d["DEPLOY"]
                ulakbus_service.save()

environ['PYOKO_SETTINGS'] = 'ulakbus.settings'
environ['ZENGINE_SETTINGS'] = 'ulakbus.settings'

if __name__ == '__main__':
    ManagementCommands()
