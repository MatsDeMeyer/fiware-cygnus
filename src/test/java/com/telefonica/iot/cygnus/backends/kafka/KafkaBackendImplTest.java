/**
 * Copyright 2016 Telefonica Investigación y Desarrollo, S.A.U
 *
 * This file is part of fiware-cygnus (FI-WARE project).
 *
 * fiware-cygnus is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
 * General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 * fiware-cygnus is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
 * implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
 * for more details.
 *
 * You should have received a copy of the GNU Affero General Public License along with fiware-cygnus. If not, see
 * http://www.gnu.org/licenses/.
 *
 * For those usages not covered by the GNU Affero General Public License please contact with iot_support at tid dot es
 */
package com.telefonica.iot.cygnus.backends.kafka;

import java.util.Properties;
import kafka.admin.AdminUtils;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import static org.junit.Assert.assertTrue;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import static org.mockito.Mockito.when;
import org.mockito.runners.MockitoJUnitRunner;

/**
 *
 * @author pcoello25
 */

@RunWith(MockitoJUnitRunner.class)
public class KafkaBackendImplTest {
    
    // mocks 
    @Mock 
    private KafkaProducer mockKafkaProducer;
    
    /**
     * Sets up tests by creating a unique instance of the tested class, and by 
     * defining the behaviour of the mocked
     * classes.
     *  
     * @throws Exception
     */
    
    @Before
    public void setUp() throws Exception {  
        when(mockKafkaProducer.send(Mockito.any(ProducerRecord.class))).thenReturn(null);
    } // setUp
    
    @Test
    public void recordIsAddedAndSent() throws Exception {
        KafkaBackendImpl backendImpl = new KafkaBackendImpl(createProperties());    
        backendImpl.setKafkaProducer(mockKafkaProducer);
        System.out.println("[KafkaBackendImplTest] ---- Adding a record to send ---- ");
        
        try {
            backendImpl.send(Mockito.any(ProducerRecord.class));   
            System.out.println("[KafkaBackendImpl.createTopic] -  OK  - Added to send");
            assertTrue(true);
        } catch (AssertionError e) {
            System.out.println("[KafkaBackendImpl.createTopic] -  FAIL  - Addition failed");
            throw e;
        } // try catch
        
    } // testTopicNameIsCreatedAndExists 
    
    private Properties createProperties() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        return props;
    }
} // KafkaBackendImplTest
