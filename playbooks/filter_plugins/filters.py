#!/usr/bin/python

class FilterModule(object):
    def filters(self):
        return {
            'ansibleHostnameNumber': self.ansibleHostnameNumber,
            'mysqlParityOffset': self.mysqlParityOffset,
            'instancesDirList': self.instancesDirList,
            'instanceDbName': self.instanceDbName,
            'is_in': self.is_in,
            'remove_element': self.remove_element
        }

    def ansibleHostnameNumber(self, host):
        """
            Extracts number from inventory host
            /!\ Works only with one number, not severals /!\
            eg: SQL01 or SQL 01 and not SQL01 54 656 7
        """
        digit = ""

        for c in host:
            if c.isdigit():
                digit += c

        return int(digit)

    def mysqlParityOffset(self, host):
        """
            Gets the auto_increment_offset number according to the ansible_hostname
        """
        host_number = self.ansibleHostnameNumber(host)

        parity = host_number % 2

        """
            If we've got an odd number (1 because something % 2 is always 0 or 1)
            then we return this number
        """
        if parity != 0:
            return parity

        """
            Otherwise we are in an even number case which is 0 and we just have to
            return 2
        """
        return 2

    def instancesDirList(self, instances_rep):
        """
            Gets a list of instances from instances_rep
            It will only replace "prod" with mediboard
        """
        instances = list()
        for _instance in instances_rep:
            if _instance["name"] == "prod":
                tmp_instance = _instance
                tmp_instance["name"] = "mediboard"
                instances.append(tmp_instance)
            else:
                instances.append(_instance)
            
        return instances

    def instanceDbName(self, instance_name):
        """
            This method ONLY purpose is to checkout if
            the instance_name parameter is equal to mediboard.
            In that case, it will return prod, otherwise, it
            will return instance_name
        """

        if instance_name == "mediboard":
            return "prod"
        
        if instance_name.find("-") != -1 or instance_name.find("_") != -1:
            separator_location_underscore = instance_name.find("_") 
            separator_location_hyphen = instance_name.find("-")

            if separator_location_underscore == -1 and separator_location_hyphen != -1:
                separator_location = separator_location_hyphen
            elif separator_location_underscore != -1 and separator_location_hyphen == -1:
                separator_location = separator_location_underscore
            else:
                separator_location = min(separator_location_hyphen, separator_location_underscore)
           
            instance_name = instance_name[:separator_location]

        # We cut the string if it is more than 7 caracters long
        if len(instance_name) > 7:
            instance_name = instance_name[:7]
        
        return instance_name

    def is_in(self, needle, stack, dict_attribute):
        """
            This method looks for needle in stack[i][dict_attribute]
        """
        for index, _item in enumerate(stack):
            if dict_attribute in _item:
                if needle == _item[dict_attribute]:
                    return True
        return False

    def remove_element(self, needle, stack, dict_attribute):
        """
            This method removes needle from stack according to dict attribute
            YES, it's a filter class and this method is NOT supposed to be there.
            It will be removed when a dedicated module will be created
        """
        for _index, _item in enumerate(stack):
            if dict_attribute in _item:
                if needle == _item[dict_attribute]:
                    del stack[_index]
                    return True
        return False

        

