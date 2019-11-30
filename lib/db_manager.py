import sqlite3.dbapi2 as sqlite3
import numbers
class database_engine:

    def __init__(self,nomefiledb):
        try:
            self.db_filename = nomefiledb
            #creo la connessione al database
            self.conn = sqlite3.connect(self.db_filename, check_same_thread = False)
            #creo un cursore
            self.c = self.conn.cursor()
            self.need_update = False
        except Exception,e:
            print 'ERRORE NELLA CONNESSIONE AL DB'
            print e
            self.c.close()
            self.conn.close()

    def ritorna_connessione(self):
        connessione = self.conn
        return connessione
    #############################################
    #### FUNZIONE DI CONNESSIONE AL DATABASE ####
    #############################################
    #def connessione_db(self):
        #global db_filename,conn,c
    #    try:
            #creo la connessione al database
    #        self.conn = sqlite3.connect(self.db_filename, check_same_thread = False)
            #creo un cursore
    #        self.c = self.conn.cursor()
    #        self.need_update = False
    #    except Exception,e:
    #        print 'ERRORE NELLA CONNESSIONE AL DB'
    #        print e
    #        self.c.close()
    #        self.conn.close()
    ##################################################
    #### FUNZIONE DI SCRITTURA DI UN SINGOLO DATO ####
    ##################################################
    def scrittura_singola_db(self,tabella,colonna,indice_ID,dato_scrivere):
        #global c,conn
        try:
            #print 'SCRITTURA SINGOLO DATO' + tabella + ' ' + colonna + ' ' + indice_ID + ' ' + dato_scrivere
            self.c.execute("""UPDATE '%s' set '%s' = %d where ID='%s'""" % (tabella, colonna, dato_scrivere, indice_ID))
            #conn.commit()
            #ATTENZIONE RICORDARSI DI FARE IL COMMIT!!!
        except Exception,e:
            print 'ERRORE NELLA SCRITTURA DEL SINGOLO DATO'
            print e
            self.c.close()
            self.conn.close()
    ################################################
    #### FUNZIONE DI LETTURA DI UN SINGOLO DATO ####
    ################################################
    def lettura_singolo_dato(self,tabella,colonna,indice_ID):
        #global c,conn
        try:
            if isinstance(indice_ID, numbers.Number):
                self.c.execute("""SELECT %s FROM '%s' where ID=%d""" % (colonna,tabella,indice_ID))
            else:
                self.c.execute("""SELECT %s FROM '%s' where ID='%s'""" % (colonna,tabella,indice_ID))
            #conn.commit()
            dato_letto = self.c.fetchone()
            return dato_letto
        except Exception,e:
            print 'ERRORE NELLA LETTURA DEL SINGOLO DATO'
            print e
            self.c.close()
            self.conn.close()
    ################################################
    #### FUNZIONE DI LETTURA DI DATI MULTIPLI   ####
    ################################################
    def lettura_dato_multiplo(self,tabella,colonna):
        #global c,conn
        try:
            self.c.execute("""SELECT %s FROM '%s'""" % (colonna,tabella))
            #conn.commit()
            dato_letto = self.c.fetchall()
            return dato_letto
        except Exception,e:
            print 'ERRORE NELLA LETTURA DEL SINGOLO DATO'
            print e
            self.c.close()
            self.conn.close()
    ##########################################
    #### FUNZIONE DI SALVATAGGIO DEI DATI ####
    ##########################################
    def salva_dati(self):
        #global c,conn
        try:
            self.conn.commit()
        except Exception,e:
            print 'ERRORE NEL SALVATAGGIO DEI DATI'
            print e
            self.c.close()
            self.conn.close()

    ###################################################
    #### FUNZIONE DI INSERZIONE DI UN NUOVO RECORD ####
    ###################################################
    def inserisciRecord(self,recordInserire,timeStamp):
        try:
            self.c.execute("SELECT COUNT(*) FROM errorList")
            lastRow = self.c.fetchone()[0]
            i = lastRow + 1
            self.c.execute("INSERT INTO errorList (ID,ERRORE,TIMESTAMP) VALUES (?,?,?)",(i,str(recordInserire),str(timeStamp)))
        except Exception,e:
            print 'ERRORE NEL INSERIMENTO DI UN RECORD'
            print e
    ###################################################
    #### FUNZIONE DI INSERZIONE DI UN NUOVO RECORD ####
    ###################################################
    def inserisciEvento(self,eventoInserire,timeStamp):
        try:
            self.c.execute("SELECT COUNT(*) FROM eventList")
            lastRow = self.c.fetchone()[0]
            i = lastRow + 1
            self.c.execute("INSERT INTO eventList (ID,EVENTO,TIMESTAMP) VALUES (?,?,?)",(i,str(eventoInserire),str(timeStamp)))
        except Exception,e:
            print 'ERRORE NEL INSERIMENTO DI UN EVENTO'
            print e

    ############################################################
    #### FUNZIONE DI INSERZIONE DI UN NUOVO VALORE DI TREND ####
    ############################################################
    def inserisciTrendValue(self,nomeTabella,value):
        try:
            self.c.execute('SELECT COUNT(*) FROM "{0}"'.format(nomeTabella))
            lastRow = self.c.fetchone()[0]
            #print 'ultima posizione scritta:',lastRow
            i = lastRow + 1
            #print 'posizione di scrittura:',i
            #print 'valore da inserire:', value
            self.c.execute('INSERT INTO "{0}" (ID,Value) VALUES ({1},{2})'.format(nomeTabella,i,value))
        except Exception,e:
            print 'ERRORE NEL INSERIMENTO DI UN NUOVO VALORE TREND'
            print e

    #####################################################
    #### FUNZIONE DI AGGIORNAMENTO TEMPERATURA       ####
    #####################################################
    def scriviTemperatura(self,value,nomeStanza):
        try:
            self.c.execute("""UPDATE temperature set valore=%d where ID='%s'""" % (value,nomeStanza))
        except Exception,e:
            print 'ERRORE NEL AGGIORNAMENTO DEL VALORE DI TEMPERATURA'
            print e
    #####################################################
    #### FUNZIONE DI CANCELLAZIONE DI TUTTI I RECORD ####
    #####################################################
    def cancellaTuttiRecords(self,nomeTabella):
        try:
            self.c.execute('DELETE FROM "{0}"'.format(nomeTabella))
        except Exception,e:
            print 'ERRORE NELLA CANCELLAZIONE DEI RECORD'
            print e

    #######################################################
    #### FUNZIONE DI SCRITTURA DI UN ARRAY SU DATABASE ####
    #######################################################
    def scritturaArray(self,nomeTabella,arrayTemp):
        try:
            for (i, item) in enumerate(arrayTemp):
                temp_dato = arrayTemp[i]
                self.c.execute('INSERT INTO "{0}" (ID,Value) VALUES ({1},{2})'.format(nomeTabella,i,temp_dato))
        except Exception,e:
            print 'ERRORE NELLA FUNZIONE DI SCRITTURA ARRAY SU DATABASE'
            print e
        
    ###################################
    #### FUNZIONE DI SCRITTURA I/O ####
    ###################################
    def scrittura_io_db(self,ingressi_1,ingressi_2,ingressi_3,ingressi_4,uscite_1,uscite_2,uscite_3,uscite_4):
        #global c,conn
        try:
            ############################################
            #### INIZIO SCRITTURA DATI NEL DATABASE ####
            ############################################
            print 'SCRITTURA INGRESSI SCHEDA 1 NEL DATABASE'
            for (i, item) in enumerate(ingressi_1):
                temp_dato = ingressi_1[i]
                self.c.execute("""UPDATE rasp_data set ingressi=%d where ID=%d""" % (temp_dato,i))
            self.conn.commit()
        except Exception,e:
            print 'ERRORE NELLA SCRITTURA DEGLI INGRESSI SCHEDA 1 NEL DATABASE'
            print e
        try:
            print 'SCRITTURA INGRESSI SCHEDA 2 NEL DATABASE'
            for (i, item) in enumerate(ingressi_2):
				temp_dato = ingressi_2[i]
				self.c.execute("""UPDATE rasp_data set ingressi=%d where ID=%d""" % (temp_dato,i + 8))
            self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DEGLI INGRESSI SCHEDA 2 NEL DATABASE'
			print e
        try:
			print 'SCRITTURA INGRESSI SCHEDA 3 NEL DATABASE'
			for (i, item) in enumerate(ingressi_3):
				temp_dato = ingressi_3[i]
				self.c.execute("""UPDATE rasp_data set ingressi=%d where ID=%d""" % (temp_dato,i + 16))
			self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DEGLI INGRESSI SCHEDA 3 NEL DATABASE'
			print e
        try:
			print 'SCRITTURA INGRESSI SCHEDA 4 NEL DATABASE'
			for (i, item) in enumerate(ingressi_4):
				temp_dato = ingressi_4[i]
				self.c.execute("""UPDATE rasp_data set ingressi=%d where ID=%d""" % (temp_dato,i + 24))
			self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DEGLI INGRESSI SCHEDA 4 NEL DATABASE'
			print e
        try:
			print 'SCRITTURA USCITE SCHEDA 1 NEL DATABASE'
			for (i, item) in enumerate(uscite_1):
				temp_dato = uscite_1[i]
				self.c.execute("""UPDATE rasp_data set uscite='%r' where ID=%d""" % (temp_dato,i))
			self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DELLE USCITE SCHEDA 1 NEL DATABASE'
			print e
        try:
            print 'SCRITTURA USCITE SCHEDA 2 NEL DATABASE'
            for (i, item) in enumerate(uscite_2):
				temp_dato = uscite_2[i]
				self.c.execute("""UPDATE rasp_data set uscite='%r' where ID=%d""" % (temp_dato,i + 8))
            self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DELLE USCITE SCHEDA 2 NEL DATABASE'
			print e
        try:
			print 'SCRITTURA USCITE SCHEDA 3 NEL DATABASE'
			for (i, item) in enumerate(uscite_3):
				temp_dato = uscite_3[i]
				self.c.execute("""UPDATE rasp_data set uscite='%r' where ID=%d""" % (temp_dato, i + 16))
			self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DELLE USCITE SCHEDA 3 NEL DATABASE'
			print e
        try:
			print 'SCRITTURA USCITE SCHEDA 4 NEL DATABASE'
			for (i, item) in enumerate(uscite_4):
				temp_dato = uscite_4[i]
				self.c.execute("""UPDATE rasp_data set uscite='%r' where ID=%d""" % (temp_dato, i + 24))
			self.conn.commit()
        except Exception,e:
			print 'ERRORE NELLA SCRITTURA DELLE USCITE SCHEDA 4 NEL DATABASE'
			print e
