import sys

from uplink_python.errors import BucketNotEmptyError
from uplink_python.errors import BucketNotFoundError
from uplink_python.errors import StorjException
from uplink_python.module_classes import ListObjectsOptions
from uplink_python.uplink import Uplink

variable_name = Uplink()

# pylint: disable=too-many-arguments
""" example project for storj-python binding shows how to use binding for various tasks. """

from datetime import datetime

class UplinkService:

    def __init__(self,
                 ACCESS_CODE = "secret_code"):
        # create an object of Uplink class
        self.uplink = Uplink()

        # function calls
        # request access using passphrase
        #print("\nRequesting Access using passphrase...")
        self.access = self.uplink.parse_access(
                serialized_access = ACCESS_CODE)
        #print("Request Access: SUCCESS!")
        #

        # open Storj project
        #print("\nOpening the Storj project, corresponding to the parsed Access...")
        self.project = self.access.open_project()
        #print("Desired Storj project: OPENED!")

    def list_buckets(self):

        try:
            # enlist all the buckets in given Storj project
            print("\nListing bucket's names and creation time...")
            bucket_list = self.project.list_buckets()
            for bucket in bucket_list:
                # as python class object
                print(bucket.name, " | ", datetime.fromtimestamp(bucket.created))
                # as python dictionary
                print(bucket.get_dict())
            print("Buckets listing: COMPLETE!")
        except StorjException as exception:
            print("Exception Caught: ", exception.details)

    def delete_bucket(self, BUCKET_NAME):
        # delete given bucket
        print("\nDeleting '" + BUCKET_NAME + "' bucket...")
        try:
            self.bucket = self.project.delete_bucket(BUCKET_NAME)
        # if delete bucket fails due to "not empty", delete all the objects and try again
        except BucketNotEmptyError as exception:
            print("Error while deleting bucket: ", exception.message)
            print("Deleting object's inside bucket and try to delete bucket again...")
            # list objects in given bucket recursively using ListObjectsOptions
            print("Listing and deleting object's inside bucket...")
            objects_list = self.project.list_objects(BUCKET_NAME, ListObjectsOptions(recursive = True))
            # iterate through all objects path
            for obj in objects_list:
                # delete selected object
                print("Deleting '" + obj.key)
                _ = self.project.delete_object(BUCKET_NAME, obj.key)
            print("Delete all objects inside the bucket : COMPLETE!")

            # try to delete given bucket
            print("Deleting '" + BUCKET_NAME + "' bucket...")
            _ = self.project.delete_bucket(BUCKET_NAME)
            print("Desired bucket: DELETED")
        except BucketNotFoundError as exception:
            print("Desired bucket delete error: ", exception.message)

    def create_bucket(self, BUCKET_NAME):
        try:
            # create bucket in given project
            print("\nCreating '" + BUCKET_NAME + "' bucket...")
            _ = self.project.create_bucket(BUCKET_NAME)
            print("Desired Bucket: CREATED!")
        except StorjException as exception:
            print("Exception Caught: ", exception.details)

    def upload_file(self, file_path, filename, BUCKET_NAME):
        try:
            print("\nUploading data...")
            # get handle of file to be uploaded
            file_handle = open(file_path, 'r+b')
            # get upload handle to specified bucket and upload file path
            MY_STORJ_UPLOAD_PATH = filename
            upload = self.project.upload_object(BUCKET_NAME, MY_STORJ_UPLOAD_PATH)
            #
            # upload file on storj
            upload.write_file(file_handle)
            #
            # commit the upload
            upload.commit()
            # close file handle
            file_handle.close()
            print("Upload: COMPLETE!")
        except StorjException as exception:
            print("Exception Caught: ", exception.details)

    def upload_binary_file(self, data, filename, BUCKET_NAME):

        try:
            # get handle of file to be uploaded
            # get upload handle to specified bucket and upload file path
            MY_STORJ_UPLOAD_PATH = filename
            upload = self.project.upload_object(BUCKET_NAME, MY_STORJ_UPLOAD_PATH)

            #
            # upload file on storj
            upload.write_file(data)

            #
            # commit the upload
            upload.commit()
            """print("ciao")
            sys.stdout.flush()"""
        except Exception as exception:
            print(exception)
            sys.stdout.flush()

    def list_bucket_objects(self, BUCKET_NAME):
        try:
            # list objects in given bucket with above options or None
            print("\nListing object's names...")
            objects_list = self.project.list_objects(BUCKET_NAME, ListObjectsOptions(recursive = True,
                                                                                     system = True))
            # print all objects path
            print(len(objects_list))
            """for obj in objects_list:
                print(obj.key, " | ", obj.is_prefix)  # as python class object
                print(obj.get_dict())  # as python dictionary
            print("Objects listing: COMPLETE!")
            #"""
        except StorjException as exception:
            print("Exception Caught: ", exception.details)

    def download_object(self, BUCKET_NAME, REMOTE_FILENAME, local_filename):
        try:
            # as an example of 'get' , lets download an object and write it to a local file
            # download file/object
            print("\nDownloading data...")
            # get handle of file which data has to be downloaded
            file_handle = open(local_filename, 'w+b')
            # get download handle to specified bucket and object path to be downloaded
            download = self.project.download_object(BUCKET_NAME, REMOTE_FILENAME)
            #
            # download data from storj to file
            download.read_file(file_handle)
            #
            # close the download stream
            download.close()
            # close file handle
            file_handle.close()
            print("Download: COMPLETE!")
        except StorjException as exception:
            print("Exception Caught: ", exception.details)

if __name__ == "__main__":


    # Source and destination path and file name for testing

    us = UplinkService()

    import requests
    from io import BytesIO
    url = "https://www.key4biz.it/wp-content/uploads/2022/03/Key4biz-SOSenergia-31-marzo.jpg"
    response = requests.get(url)
    image_data = BytesIO(response.content)


    us.list_buckets()
    # us.delete_bucket(BUCKET_NAME = 'incidents-images')
    #us.create_bucket(BUCKET_NAME = 'incidents-images')
    # us.upload_binary_file(data =image_data, filename = "wow22.jpg", BUCKET_NAME = "incidents-images")
    us.list_bucket_objects(BUCKET_NAME = "incidents-images")