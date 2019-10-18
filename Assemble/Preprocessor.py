# python3
# -*- coding: utf-8 -*-
# @File    : Preprocessor.py
# @Desc    :
# @Project : MIPSAssembler
# @Time    : 10/17/19 7:58 PM
# @Author  : Loopy
# @Contact : peter@mail.loopy.tech
# @License : CC BY-NC-SA 4.0 (subject to project license)

import re


class Preprocessor:
    def __init__(self):
        raise SyntaxError("Preprocessor can not instance, please use static method")

    @staticmethod
    def prep(mips_code, return_label=True):

        mips_code = re.sub("#.+?\n", "\n", mips_code)  # remove annotation
        mips_code = re.sub("\n+", "\n", mips_code)  # remove empty line
        mips_code = re.sub(" +", " ", mips_code)  # remove redundant space
        mips_code = re.sub("\n | \n", "\n", mips_code)  # remove space at line_start_end

        inst_list = mips_code.split("\n")

        # deal with jump label
        label = {}
        index = 0
        while True:
            if inst_list[index] == "":
                del inst_list[index]
            elif ":" not in inst_list[index]:
                index += 1
            else:
                this_line = inst_list[index].split(":")
                label[this_line[0]] = index
                if len(this_line) > 1:
                    inst_list[index] = this_line[1]
                else:
                    del inst_list[index]
            if index >= len(inst_list):
                break

        if return_label:
            return inst_list, label
        else:
            return inst_list

    @staticmethod
    def prep_line(mips_line):
        if ":" not in mips_line:
            return list(
                filter(
                    lambda x: x != "",
                    mips_line.replace(",", " ")
                    .replace("(", " ")
                    .replace(")", "")
                    .split(" "),
                )
            ),None
        else:
            this_line = mips_line.split(":")
            if len(this_line) > 1:
                return (
                    list(
                        filter(
                            lambda x: x != "",
                            this_line[1].replace(",", " ")
                            .replace("(", " ")
                            .replace(")", "")
                            .split(" "),
                        )
                    ),
                    this_line[0],
                )
            else:
                return None, this_line[0]