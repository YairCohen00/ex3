import re
import json


def id_maker(chats):
    x = 1
    ids = {}
    for line in chats:
        if (" - " and ": ") in line:
            l = line.strip()
            indexstart = l.find(" - ") + 3
            indexend = l.find(": ")
            name = l[indexstart:indexend]
            if name not in ids:
                ids[name] = x
                x += 1
    return ids


def id_macth(name, ids):
    id = ids[name]
    return id


def name_finder(line):
    indexstart = line.find(" - ") + 3
    indexend = line.find(": ")
    name = line[indexstart:indexend]
    return name


def text_finder(line):
    textStart = line.find(": ")
    text = line[textStart + 2:]
    return text


def date_finder(line):
    date = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+, [0-9]+:[0-9]+", line)
    return date[0]


def messages_maker(chats):
    ids = id_maker(chats)
    messages = []
    for line in chats:
        if not bool(re.match(r"[0-9]+\.[0-9]+\.[0-9]+, [0-9]+:[0-9]+", line)):
            temp = line.strip()
            temp = messages[-1]['text'] + "\n" + temp
            messages[-1]['text'] = temp
            continue
        if ": " not in line:
            continue
        l = line.strip()
        date = date_finder(l)
        text = text_finder(l)
        name = name_finder(l)
        id = id_macth(name, ids)
        msg = {'datetime': date, 'id': id, 'text': text}
        messages.append(msg)
    return messages


def meatadata_maker(chats):
    group_name_start = chats[1].find("\"") + 1
    group_name_end = chats[1].rfind("\"")
    group_name = chats[1][group_name_start:group_name_end]
    creation_date = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+, [0-9]+:[0-9]+", chats[1])[0]

    participants = "<" + str(len(id_maker(chats))) + ">"
    creator = chats[1].split("ידי ")[1].strip()
    metadata = {"chat_name": group_name, "creation_date": creation_date, "num_of_participants": participants,
                "creator": creator}
    return metadata


def whatsapp_dic_maker(messages, metadata):
    whatsapp = {"messages": messages_maker(chats), "metadata": meatadata_maker(chats)}
    return whatsapp


def whatsapp_to_json_output(whatsapp):
    group_name = whatsapp['metadata']['chat_name']
    outputfile = open(group_name + ".txt", 'w', encoding='utf8')
    outputfile.write(json.dumps(whatsapp, indent=4, ensure_ascii=False))
    outputfile.close()


file = open("�צאט WhatsApp עם יום הולדת בנות לנויה.txt", encoding='utf-8')
chats = file.readlines()
file.close()
messages = messages_maker(chats)
metadata = meatadata_maker(chats)
whatsapp = whatsapp_dic_maker(messages, metadata)
whatsapp_to_json_output(whatsapp)
