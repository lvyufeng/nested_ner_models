import json
import os
import signal
class Modifier():
    def __init__(self, path, save_path):
        self.data_path = {
            'train': os.path.join(path, 'train.txt'),
            'dev': os.path.join(path, 'dev.txt'),
            'test': os.path.join(path, 'test.txt')
        }
        self.save_path = save_path
        self.process = {}
        self.all_entities = {}
    def _exit(self,signum, frame):
        self._save_json(os.path.join(self.save_path, 'entities.json'))
        exit()
    def _read_single_file(self, file_path):
        data = []
        with open(file_path, encoding='utf-8') as f:
            for i in f.readlines():
                data.append(i)
        f.close()
        return data
    def _read_all_data(self):
        data = []
        for i in self.data_path.keys():
            data.extend(self._read_single_file(self.data_path[i]))
        return data

    def _bio2json(self,data):
        sentences = []
        sentence = ''
        entities = []
        entity = ''
        entity_type = ''
        for i in data:
            i = i.strip()
            if i == '':
                if entity != '':
                    entities.append({
                        'type':entity_type,
                        'entity':entity
                    })
                    entity = ''
                    entity_type = ''
                for e in entities:
                    e['text'] = sentence
                    e['begin'] = sentence.find(e['entity'])
                    e['end'] = e['begin'] + len(e['entity'])
                    sentences.append(e)
                sentence = ''
                entities = []
                continue
            token, tag = i.split(' ')
            sentence = sentence + token
            if tag != 'O':
                entity = entity + token
                entity_type = tag.split('-')[-1]
            else:
                if entity != '':
                    entities.append({
                        'type':entity_type,
                        'entity':entity
                    })
                    entity = ''
                    entity_type = ''
        return sentences
    
    def get_all_entities(self):
        entities = self._bio2json(self._read_all_data())
        for i in entities:
            if i['type'] not in self.all_entities:
                self.all_entities[i['type']] = [i]
            else:
                self.all_entities[i['type']].append(i)
        for i in self.all_entities.keys():
            print(i,len(self.all_entities[i]))
        self._save_json(os.path.join(self.save_path, 'entities.json'))
    def _save_json(self, path):
        with open(path,'w+',encoding='utf-8') as f:
            json.dump(self.all_entities, f, ensure_ascii=False)
        f.close()
    def _check_conditions(self, entity, conditions):
        for i in conditions:
            if i in entity:
                return True
        return False

    def _check_one_type(self, entity_type):
        conditions = input('input conditions, split by "," :')
        conditions = [i for i in conditions.split(',')]
        length = len(self.all_entities[entity_type])
        for idx, i in enumerate(self.all_entities[entity_type]):
            if self._check_conditions(i['entity'], conditions):
                self.all_entities[entity_type][idx]['flag'] = True
                continue
            os.system('clear')
            print('working on {} of {}'.format(idx,length))
            print('text: ' + i['text'])
            print('entity: {}, type: {}'.format(i['entity'],entity_type))
            flag = input('entity type is right:')
            if flag == 'y':
                self.all_entities[entity_type][idx]['flag'] = True
            else:
                self.all_entities[entity_type][idx]['flag'] = False



data_path = '/Users/lvyufeng/PycharmProjects/nested_ner_models/raw_noisy_data'
save_path = '/Users/lvyufeng/PycharmProjects/nested_ner_models/preprocessing'
modifier = Modifier(data_path, save_path)
signal.signal(signal.SIGINT, modifier._exit)
signal.signal(signal.SIGHUP, modifier._exit)
signal.signal(signal.SIGTERM, modifier._exit)
modifier.get_all_entities()
modifier._check_one_type('MDL')