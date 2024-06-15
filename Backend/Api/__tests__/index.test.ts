import * as request from 'supertest';
import app from '../src/index';

describe('POST /run', () => {
    it('should return 200 OK', () => {
        return request(app).post('/run').expect(200);
    });
});
